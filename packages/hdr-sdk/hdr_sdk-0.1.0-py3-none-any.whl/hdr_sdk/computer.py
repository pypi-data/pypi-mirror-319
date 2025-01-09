import asyncio
import base64
import json
import logging
import os
from datetime import datetime
from typing import Any, Callable, Optional

import websockets
from pydantic import BaseModel, Field

from hdr_sdk.exceptions import ComputerNotConnected, ComputerTimeout

from .schemas import ComputerMessage, HDRConfig, MachineMetadata
from .schemas.action import Action
from .tools import ComputerTool, bash_tool, computer_tool, edit_tool

logger = logging.getLogger(__name__)


class ComputerLogger(BaseModel):
    """Logger for computer interactions and screenshots."""

    # Configuration
    base_dir: str = Field(alias="base_dir", default="computer_logs")
    conversation_file: str = "conversation.jsonl"

    # Runtime paths
    run_dir: Optional[str] = Field(alias="run_dir", default=None)
    conversation_log_file: Optional[str] = Field(alias="conversation_log_file", default=None)

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        # Set up logging directory structure
        if self.run_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.run_dir = os.path.join(self.base_dir, timestamp)

        self.conversation_log_file = os.path.join(self.run_dir, self.conversation_file)

        # Ensure directories exist
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.run_dir, exist_ok=True)

    def log_send(self, command: dict) -> None:
        """Log a command to the conversation log."""

        with open(self.conversation_log_file, "a") as f:
            f.write(json.dumps(command) + "\n")

    def log_receive(self, message: ComputerMessage) -> None:
        """Log a computer message and any associated screenshots."""
        screenshot_file = self._log_screenshot(message)
        message_dict = message.model_dump(mode="json")
        message_dict["tool_result"]["screenshot_file"] = screenshot_file
        message_dict["tool_result"].pop("base64_image")

        with open(self.conversation_log_file, "a") as f:
            f.write(json.dumps(message_dict) + "\n")

    def _log_screenshot(self, message: ComputerMessage) -> str | None:
        """Save screenshot from message if present and return the file path."""
        if message.tool_result.base64_image:
            screenshot_file = os.path.join(self.run_dir, f"screenshot_{message.metadata.response_timestamp}.png")
            with open(screenshot_file, "wb") as f:
                f.write(base64.b64decode(message.tool_result.base64_image))
            return screenshot_file
        return None

    def cleanup(self) -> None:
        """Remove all files in the run directory."""
        for file in os.listdir(self.run_dir):
            os.remove(os.path.join(self.run_dir, file))
        os.rmdir(self.run_dir)


class Computer:
    """
    Main class for managing computer control operations through WebSocket
    """

    def __init__(self, options: Optional[dict[str, Any]] = None):
        self.options = self._merge_default_options(options or {})
        self.config = HDRConfig(base_url=options.get("base_url"), api_key=options.get("api_key"))
        self.logger = ComputerLogger()
        self.created_at = datetime.now().isoformat()
        self.updated_at: Optional[str] = None
        self.session_id: Optional[str] = None
        self.machine_metadata: Optional[MachineMetadata] = None
        self.ws: Optional[websockets.ClientProtocol] = None
        self.tools: list[ComputerTool] = self.options["tools"]

    @staticmethod
    def _merge_default_options(options: dict[str, Any]) -> dict[str, Any]:
        """Merge provided options with defaults"""
        default_options = {
            "base_url": "wss://api.hdr.is/compute/ephemeral",
            "tools": [bash_tool, computer_tool, edit_tool],
            "on_open": lambda: None,
            "on_message": lambda _: None,
            "on_error": lambda _: None,
            "on_close": lambda _, __: None,
            "parse_message": lambda message: ComputerMessage.model_validate_json(message),
            "before_send": lambda data: data,
        }
        return {**default_options, **options}

    async def connect(self) -> None:
        """Establishes WebSocket connection"""
        headers = {"Authorization": f"Bearer {self.config.api_key}"}

        try:
            import websockets

            self.ws = await websockets.connect(self.config.base_url, additional_headers=headers)
            if self.options["on_open"]:
                await self._maybe_await(self.options["on_open"])

            first_message = await self.ws.recv()
            self._handle_connection_message(ComputerMessage.model_validate_json(first_message))

        except Exception as e:  # noqa: F841
            logger.error("Connection failed", exc_info=True)
            raise

    async def _handle_message(self, message: str) -> None:
        """Process incoming WebSocket messages"""
        try:
            parsed_message = ComputerMessage.model_validate_json(message)
            self._set_updated_at(parsed_message.metadata.response_timestamp)
            self.logger.log_receive(parsed_message)
            return parsed_message  # noqa: TRY300
        except Exception as e:
            await self._handle_error(e)
            return None

    def _handle_connection_message(self, message: ComputerMessage) -> None:
        """Process connection-related messages and update machine metadata"""
        self.logger.log_receive(message)
        try:
            machine_metadata = MachineMetadata.model_validate_json(message.tool_result.system)
            self.machine_metadata = machine_metadata
            self.session_id = message.metadata.session_id

            updated_computer_tool = {
                **computer_tool,
                "display_height_px": machine_metadata.display_height or 0,
                "display_width_px": machine_metadata.display_width or 0,
            }

            # Replace the old computer_tool with the updated one
            for i, tool in enumerate(self.tools):
                if tool["name"] == "computer":
                    self.tools[i] = updated_computer_tool
                    break
        except Exception:
            logger.exception("Failed to handle connection message")
            pass  # Not a connection message

    async def _handle_error(self, error: Exception) -> None:
        """Handle WebSocket errors"""
        logger.error(f"Error: {error!s}")
        await self._maybe_await(self.options["on_error"], error)

    async def execute(self, command: Action) -> ComputerMessage:
        """Execute a command and wait for response"""
        await self._ensure_connected()

        # Create a plain dict without any extra processing
        command_data = {"tool": command.tool, "params": command.params}

        logger.info("Sending command: %s", command_data)
        await self._send(command_data)

        # Wait for response with timeout
        try:
            response = await asyncio.wait_for(self.ws.recv(), timeout=30.0)
            return await self._handle_message(response)
        except asyncio.TimeoutError as err:
            raise ComputerTimeout() from err

    async def _send(self, data: dict[str, Any]) -> None:
        """Send data through WebSocket connection"""
        if not self.ws or not self.is_connected():
            raise ComputerNotConnected()

        # Convert Pydantic models to plain dicts
        if hasattr(data, "model_dump"):
            data = data.model_dump()

        # Ensure we're working with a plain dict
        message = json.dumps(data, separators=(",", ":"))
        await self.ws.send(message)
        self.logger.log_send(data)

    async def do(self, objective: str, provider: str = "anthropic") -> None:
        """Execute a high-level objective using specified provider"""
        if provider != "anthropic":
            raise ValueError(  # noqa: TRY003
                "Custom providers are not supported for this method. " "Use the execute method instead."
            )
        from .anthropic import use_computer

        await use_computer(objective, self)

    async def screenshot(self) -> str:
        """Take a screenshot of the connected computer"""
        message = await self.execute(Action(tool="computer", params={"action": "screenshot"}))

        if not message.tool_result.base64_image:
            raise Exception("No screenshot data received")  # noqa: TRY002, TRY003
        return message.tool_result.base64_image

    def register_tool(self, tools: list[ComputerTool]) -> None:
        """Register new tools for computer control"""
        for tool in tools:
            if tool not in self.tools:
                self.tools.append(tool)

    def list_tools(self) -> list[ComputerTool]:
        """List all registered tools"""
        return list(self.tools)

    def is_connected(self) -> bool:
        """Check if WebSocket connection is active"""
        return self.ws is not None and self.ws.state.name == "OPEN"

    async def close(self) -> None:
        """Close the WebSocket connection"""
        if self.ws:
            await self.ws.close()
            self.ws = None

    def _set_updated_at(self, timestamp: datetime) -> None:
        """Update the last activity timestamp"""
        self.updated_at = timestamp.isoformat()

    async def _ensure_connected(self) -> None:
        """Ensure WebSocket connection is established"""
        if not self.is_connected():
            await self.connect()

    @staticmethod
    async def _maybe_await(func: Callable, *args, **kwargs) -> Any:
        """Helper to handle both async and sync callbacks"""
        result = func(*args, **kwargs)
        if asyncio.iscoroutine(result):
            return await result
        return result
