from typing import Any

from pydantic import BaseModel

from .bash_action import BashAction
from .computer_actions import ComputerAction
from .edit_actions import EditAction


class Action(BaseModel):
    tool: str
    params: Any

    @classmethod
    def model_validate(cls, obj):
        if isinstance(obj, dict):
            if obj["tool"] == "computer":
                return ComputerAction(tool=obj["tool"], params=obj["params"])
            elif obj["tool"] == "bash":
                return BashAction(tool=obj["tool"], params=obj["params"])
            elif obj["tool"] == "edit":
                return EditAction(tool=obj["tool"], params=obj["params"])
        return super().model_validate(obj)
