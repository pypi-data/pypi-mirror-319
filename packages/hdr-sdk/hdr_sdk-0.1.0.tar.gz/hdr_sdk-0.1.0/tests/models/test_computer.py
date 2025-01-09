import asyncio
import os

import pytest
import pytest_asyncio
from dotenv import load_dotenv

from hdr_sdk.computer import Computer, ComputerLogger, ComputerMessage
from hdr_sdk.schemas.action import Action
from hdr_sdk.schemas.tool_base import ToolResult

load_dotenv()


@pytest.fixture(scope="function")
def _computer() -> Computer:
    """Create Computer instance with config."""
    return Computer({"base_url": "wss://api.hdr.is/compute/ephemeral", "api_key": os.getenv("HDR_API_KEY")})


@pytest_asyncio.fixture(scope="function")
async def computer(_computer: Computer):
    """Connect computer and yield for tests, then cleanup."""
    try:
        await _computer.connect()
        # Wait a bit for the connection to stabilize
        await asyncio.sleep(1)
        yield _computer
    finally:
        await _computer.close()


@pytest.mark.asyncio
class TestComputer:
    """Test suite for Computer class."""

    async def test_computer_created_at_is_set(self, computer: Computer) -> None:
        """Test that computer creation timestamp is set."""
        assert computer.created_at is not None

    async def test_computer_connect(self, computer: Computer) -> None:
        """Test websocket connection is established."""
        assert computer.ws is not None

    async def test_raw_input(self, computer: Computer) -> None:
        """Test raw input is sent to the computer."""
        res = await computer.ws.send('{"tool": "computer", "params": {"action": "screenshot"}}')
        assert res is not None

    async def test_screenshot(self, computer: Computer) -> None:
        """Test screenshot capture functionality."""
        try:
            screenshot = await computer.screenshot()
            assert screenshot is not None
        except Exception as e:
            pytest.fail(f"Screenshot test failed with error: {e!s}")

    async def test_execute(self, computer: Computer) -> None:
        """Test command execution functionality."""
        await asyncio.sleep(1)  # Allow connection to stabilize
        result = await computer.execute(Action(tool="bash", params={"command": "echo hello world"}))
        assert result.tool_result.output is not None
        assert "hello world" in result.tool_result.output

    def test_register_and_list_tools(self, computer: Computer) -> None:
        """Test tool registration and listing functionality."""
        initial_tools = len(computer.list_tools())
        new_tool = {"name": "test_tool", "description": "Test tool"}
        computer.register_tool([new_tool])
        assert len(computer.list_tools()) == initial_tools + 1

    def test_is_connected(self, computer: Computer) -> None:
        """Test connection status check."""
        assert computer.is_connected() is True

    @pytest.mark.asyncio
    async def test_close_connection(self, _computer: Computer) -> None:
        """Test closing the connection."""
        await _computer.connect()
        assert _computer.is_connected() is True
        await _computer.close()
        assert _computer.is_connected() is False

    @pytest.mark.asyncio
    async def test_execute_invalid_command(self, computer: Computer) -> None:
        """Test error handling for invalid command execution."""
        with pytest.raises(Exception):  # noqa: B017 TODO: fix this
            await computer.execute({"tool": "invalid_tool", "params": {}})

    @pytest.mark.asyncio
    async def test_do_invalid_provider(self, computer: Computer) -> None:
        """Test error handling for invalid provider in do method."""
        with pytest.raises(ValueError):
            await computer.do("test objective", provider="invalid_provider")


@pytest.fixture
def logger() -> ComputerLogger:
    """Create a ComputerLogger instance."""
    return ComputerLogger()


@pytest.mark.skip(reason="This test is flaky and needs to be fixed")
class TestComputerLogger:
    def test_computer_logger_logs_action(self, logger: ComputerLogger):
        """Test that computer logger logs action"""
        assert logger is not None

    def test_computer_logger_logs_conversation(self, logger: ComputerLogger):
        """Test that computer logger logs action"""
        assert logger.conversation_log_file is not None
        logger.log_send({"tool": "computer", "params": {"action": "screenshot"}})
        assert os.path.exists(logger.conversation_log_file)

    def test_computer_logger_logs_screenshot(self, logger: ComputerLogger):
        """Test that computer logger logs screenshot"""
        assert logger.conversation_log_file is not None
        logger.log_receive(
            ComputerMessage(
                session_id="test",
                timestamp=1234.5678,
                result=ToolResult(
                    base64_image="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
                ),
            )
        )
        screenshot_files = [f for f in os.listdir(logger.run_dir) if f.endswith(".png")]
        assert len(screenshot_files) > 0

    def test_computer_logger_cleanup(self, logger: ComputerLogger):
        """Test that computer logger cleanup removes all files in the run directory."""
        logger.cleanup()
        assert logger.run_dir not in os.listdir(logger.base_dir)
