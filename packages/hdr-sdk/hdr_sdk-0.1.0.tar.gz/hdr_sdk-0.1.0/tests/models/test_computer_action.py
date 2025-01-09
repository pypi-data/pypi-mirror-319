import pytest
from pydantic import ValidationError

from hdr_sdk.models.computer_action import ComputerAction, KeyAction, MouseMoveAction, TypeAction


class TestComputerAction:
    class TestLeftClickDrag:
        def test_left_click_drag_requires_coordinates(self):
            """Test that left click drag requires coordinates"""
            with pytest.raises(ValidationError):
                ComputerAction(action="left_click_drag")

        def test_left_click_drag_with_valid_coordinates(self):
            """Test that left click drag works with valid coordinates"""
            action = ComputerAction(action={"action": "left_click_drag", "coordinates": (0, 0)})
            assert action is not None

    class TestMoveMouse:
        def test_move_mouse_requires_coordinates(self):
            """Test that mouse move requires coordinates"""
            with pytest.raises(ValidationError):
                ComputerAction(action="move_mouse")

        def test_move_mouse_with_valid_coordinates(self):
            """Test that mouse move works with valid coordinates"""
            action = ComputerAction(action={"action": "mouse_move", "coordinates": (0, 0)})
            assert isinstance(action.action, MouseMoveAction)
            assert action.action.coordinates == (0, 0)

    class TestTypeAction:
        def test_type_action_requires_text(self):
            """Test that type action requires text"""
            with pytest.raises(ValidationError):
                ComputerAction(action="type")

        def test_type_action_with_valid_text(self):
            """Test that type action works with valid text"""
            action = ComputerAction(action={"action": "type", "text": "Hello, world!"})
            assert isinstance(action.action, TypeAction)
            assert action.action.text == "Hello, world!"

    class TestKeyAction:
        def test_key_action_requires_text(self):
            """Test that key action requires text"""
            with pytest.raises(ValidationError):
                ComputerAction(action="key")

        def test_key_action_with_valid_text(self):
            """Test that key action works with valid text"""
            action = ComputerAction(action={"action": "key", "text": "Enter"})
            assert isinstance(action.action, KeyAction)
            assert action.action.text == "Enter"
