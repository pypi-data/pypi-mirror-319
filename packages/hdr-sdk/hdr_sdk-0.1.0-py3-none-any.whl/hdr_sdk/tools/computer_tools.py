from typing import Literal, Optional, TypedDict, Union


class ComputerTool(TypedDict):
    name: str
    type: str
    display_height_px: Optional[int]
    display_width_px: Optional[int]


bash_tool: ComputerTool = {
    "name": "bash",
    "type": "bash_20241022",
}

computer_tool: ComputerTool = {
    "name": "computer",
    "type": "computer_20241022",
    "display_height_px": 768,
    "display_width_px": 1024,
}

edit_tool: ComputerTool = {
    "name": "str_replace_editor",
    "type": "text_editor_20241022",
}


class ImageSource(TypedDict):
    type: Literal["base64"]
    media_type: Literal["image/png"]
    data: str


class TextContent(TypedDict):
    type: Literal["text"]
    text: str


class ImageContent(TypedDict):
    type: Literal["image"]
    source: ImageSource


class ToolResult(TypedDict, total=False):
    error: Optional[str]
    output: Optional[str]
    base64_image: Optional[str]


class BetaToolResultBlockParam(TypedDict):
    type: Literal["tool_result"]
    content: list[Union[TextContent, ImageContent]]
    tool_use_id: str
    is_error: bool


def make_tool_result(result: ToolResult, tool_use_id: str) -> BetaToolResultBlockParam:
    tool_result_content: list[Union[TextContent, ImageContent]] = []
    is_error = False

    if result.error:
        is_error = True
        tool_result_content.append({"type": "text", "text": result.error})
    else:
        if result.output:
            tool_result_content.append({"type": "text", "text": result.output})
        if result.base64_image:
            tool_result_content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": "image/png", "data": result.base64_image},
            })

    return {"type": "tool_result", "content": tool_result_content, "tool_use_id": tool_use_id, "is_error": is_error}
