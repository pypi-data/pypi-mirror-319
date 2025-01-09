import logging
import os
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class HDRConfigError(Exception):
    """Error raised for HDR configuration issues."""

    pass


class HDRConfig(BaseModel):
    """Configuration for HDR API connection.

    Attributes:
        api_key: API key for authentication, loaded from HDR_API_KEY env var
        base_url: Base URL for HDR API websocket endpoint
    """

    api_key: str | None = Field(
        default_factory=lambda: os.getenv("HDR_API_KEY"), description="API key for authentication"
    )
    base_url: str = Field(default="wss://api.hdr.is/compute/ws", description="Base URL for HDR API websocket endpoint")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        logger.debug(f"HDRConfig initialized with api_key: {self.api_key}")
        self.base_url = self.base_url.rstrip("/")
        if not self.api_key:
            self.api_key = os.getenv("HDR_API_KEY")
