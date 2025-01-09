import os
from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field
from typing_extensions import TypedDict


class HDRConfig(BaseModel):
    """
    Configuration for connecting to the HDR API

    Attributes:
        api_key: API key for authentication, defaults to HDR_API_KEY env var
        base_url: WebSocket API endpoint, defaults to wss://api.hdr.is
    """

    api_key: str = Field(default_factory=lambda: os.getenv("HDR_API_KEY", ""))
    base_url: str = Field(default="wss://api.hdr.is/compute/ephemeral")
    log_dir: str = Field(default="./computer_logs")
    log_conversation: bool = Field(default=True)


class LogConfig(BaseModel):
    log_dir: str = Field(default="./computer_logs")
    run_dir: str = Field(default_factory=lambda: datetime.now().isoformat())
    log_screenshot: bool = Field(default=True)
    log_conversation: bool = Field(default=True)


class ToolResult(BaseModel):
    output: Optional[str] = None
    error: Optional[str] = None
    base64_image: Optional[str] = None
    system: Optional[str] = None


class Metadata(BaseModel):
    session_id: UUID4
    message_id: UUID4
    request_timestamp: datetime
    response_timestamp: datetime


class ComputerMessage(BaseModel):
    raw_input: str
    tool_result: ToolResult
    metadata: Metadata


class ComputerMessageLog(ComputerMessage):
    screenshot_file: Optional[str] = None


class MachineMetadata(BaseModel):
    display_height: Optional[int] = None
    display_width: Optional[int] = None
    display_num: Optional[int] = None
    arch: Optional[str] = None
    hostname: Optional[str] = None
    access_token: Optional[str] = None


class DefaultSamplingOptions(TypedDict):
    model: str
    max_tokens: int
    system: str
    messages: list[dict]  # Equivalent to BetaMessageParam
    temperature: float


default_sampling_options: DefaultSamplingOptions = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 4096,
    "temperature": 0,
    "system": "",
    "messages": [],
}
