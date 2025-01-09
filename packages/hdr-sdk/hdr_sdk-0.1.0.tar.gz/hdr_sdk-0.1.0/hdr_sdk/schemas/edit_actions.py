from enum import Enum
from typing import Annotated, Literal, Optional, Union

from pydantic import BaseModel, Field


class EditActionsEnum(str, Enum):
    view = "view"
    create = "create"
    str_replace = "str_replace"
    insert = "insert"
    undo_edit = "undo_edit"


class ViewParams(BaseModel):
    command: Literal["view"]
    path: str
    view_range: Optional[list[int]] = None

    model_config = {"json_schema_extra": {"description": "View contents of a file."}}


class CreateParams(BaseModel):
    command: Literal["create"]
    path: str
    file_text: str

    model_config = {"json_schema_extra": {"description": "Create a new file with specified content."}}


class StrReplaceParams(BaseModel):
    command: Literal["str_replace"]
    path: str
    old_str: str
    new_str: Optional[str] = None

    model_config = {"json_schema_extra": {"description": "Replace text in a file."}}


class InsertParams(BaseModel):
    command: Literal["insert"]
    path: str
    insert_line: int
    new_str: str

    model_config = {"json_schema_extra": {"description": "Insert text at specific line in a file."}}


class UndoEditParams(BaseModel):
    command: Literal["undo_edit"]
    path: str

    model_config = {"json_schema_extra": {"description": "Undo last edit to a file."}}


# Combined params using discriminated union
EditParams = Annotated[
    Union[ViewParams, CreateParams, StrReplaceParams, InsertParams, UndoEditParams], Field(discriminator="command")
]


class EditAction(BaseModel):
    tool: Literal["str_replace_editor"]
    params: EditParams

    model_config = {"json_schema_extra": {"description": "File editing operations."}}
