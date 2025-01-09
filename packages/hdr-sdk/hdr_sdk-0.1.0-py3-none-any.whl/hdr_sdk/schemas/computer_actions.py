from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field


# Custom error class
class ComputerToolError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.name = "ComputerToolError"


# Mouse Actions
class MouseMoveAction(BaseModel):
    action: Literal["mouse_move"]
    coordinate: tuple[int, int]

    model_config = {"json_schema_extra": {"description": "Move mouse cursor to specific coordinates."}}


class LeftClickDragAction(BaseModel):
    action: Literal["left_click_drag"]
    coordinates: tuple[int, int]

    model_config = {"json_schema_extra": {"description": "Click and drag with left mouse button to coordinates."}}


class CursorPositionAction(BaseModel):
    action: Literal["cursor_position"]

    model_config = {"json_schema_extra": {"description": "Get current cursor position."}}


class LeftClickAction(BaseModel):
    action: Literal["left_click"]

    model_config = {"json_schema_extra": {"description": "Perform left mouse click."}}


class RightClickAction(BaseModel):
    action: Literal["right_click"]

    model_config = {"json_schema_extra": {"description": "Perform right mouse click."}}


class MiddleClickAction(BaseModel):
    action: Literal["middle_click"]

    model_config = {"json_schema_extra": {"description": "Perform middle mouse click."}}


class DoubleClickAction(BaseModel):
    action: Literal["double_click"]

    model_config = {"json_schema_extra": {"description": "Perform double click with left mouse button."}}


# Keyboard Actions
class KeyAction(BaseModel):
    action: Literal["key"]
    text: str = Field(min_length=1, description="Text is required for key action")

    model_config = {"json_schema_extra": {"description": "Press specific keyboard key(s)."}}


class TypeAction(BaseModel):
    action: Literal["type"]
    text: str = Field(min_length=1, description="Text is required for type action")

    model_config = {"json_schema_extra": {"description": "Type text string."}}


# Screenshot Action
class ScreenshotAction(BaseModel):
    action: Literal["screenshot"]

    model_config = {"json_schema_extra": {"description": "Capture screenshot of current screen."}}


# Union of all actions using discriminated union
ComputerParams = Annotated[
    Union[
        MouseMoveAction,
        LeftClickDragAction,
        CursorPositionAction,
        LeftClickAction,
        RightClickAction,
        MiddleClickAction,
        DoubleClickAction,
        KeyAction,
        TypeAction,
        ScreenshotAction,
    ],
    Field(discriminator="action"),
]


# Container for computer control actions
class ComputerAction(BaseModel):
    tool: Literal["computer"]
    params: ComputerParams
