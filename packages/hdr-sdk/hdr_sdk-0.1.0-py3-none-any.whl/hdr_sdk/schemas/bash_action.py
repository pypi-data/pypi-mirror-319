from typing import Literal

from pydantic import BaseModel, Field


class BashActionParams(BaseModel):
    command: str = Field(min_length=1, description="Command string is required")


class BashAction(BaseModel):
    tool: Literal["bash"]
    params: BashActionParams

    model_config = {"json_schema_extra": {"description": "Execute a bash command."}}
