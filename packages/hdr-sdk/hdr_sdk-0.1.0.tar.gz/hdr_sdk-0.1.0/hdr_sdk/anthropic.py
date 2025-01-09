import logging
from datetime import datetime
from typing import Any, Optional

import anthropic
from anthropic.types.beta import (
    BetaContentBlock,
    BetaMessageParam,
    BetaTextBlockParam,
    BetaToolResultBlockParam,
    BetaToolUseBlockParam,
)

from hdr_sdk.computer import Computer
from hdr_sdk.schemas import Action, ToolResult
from hdr_sdk.schemas.config import MachineMetadata, default_sampling_options
from hdr_sdk.tools.computer_tools import make_tool_result

logger = logging.getLogger(__name__)


def system_capability(machine_metadata: MachineMetadata) -> str:
    """Generate system capability message for the computer"""
    return f"""<SYSTEM_CAPABILITY>
* You are utilising an Ubuntu virtual machine using {machine_metadata.arch} architecture with internet access.
* You can feel free to install Ubuntu applications with your bash tool. Use curl instead of wget.
* To open firefox, please just click on the firefox icon.  Note, firefox-esr is what is installed on your system.
* Using bash tool you can start GUI applications, but you need to set export DISPLAY=:1 and use a subshell. For example "(DISPLAY=:1 xterm &)". GUI apps run with bash tool will appear within your desktop environment, but they may take some time to appear. Take a screenshot to confirm it did.
* When using your bash tool with commands that are expected to output very large quantities of text, redirect into a tmp file and use str_replace_editor or `grep -n -B <lines before> -A <lines after> <query> <filename>` to confirm output.
* When viewing a page it can be helpful to zoom out so that you can see everything on the page.  Either that, or make sure you scroll down to see everything before deciding something isn't available.
* When using your computer function calls, they take a while to run and send back to you.  Where possible/feasible, try to chain multiple of these calls all into one function calls request.
* The current date is {datetime.now().strftime("%B %d, %Y")}.
</SYSTEM_CAPABILITY>"""


async def use_computer(  # noqa: C901
    task: str, computer: Computer, options: Optional[dict[str, Any]] = None
) -> None:
    """
    Executes a task on a remote computer using Claude AI and handles the interaction loop

    Args:
        task: The natural language instruction/task to give to Claude
        computer: Instance of Computer class for executing commands
        options: Optional sampling parameters for Claude (model, tokens etc)

    Raises:
        Exception: If computer connection fails
    """
    # Merge provided options with defaults
    sampling_options = {**default_sampling_options}
    if options:
        sampling_options.update(options)

    client = anthropic.Client()

    # Initialize conversation history
    messages: list[BetaMessageParam] = []

    # Add the user's task as first message
    messages.append({"role": "user", "content": task})

    # Create system prompt that tells Claude about the computer's capabilities
    system_prompt: BetaTextBlockParam = {"type": "text", "text": system_capability(computer.machine_metadata)}

    # Verify computer connection before proceeding
    if not computer.is_connected():
        raise Exception("Failed to connect to computer")  # noqa: TRY002, TRY003

    # Log available tools for debugging
    logger.info(f"Tools enabled: {computer.list_tools()}")

    # Main interaction loop
    while True:
        # Get Claude's response
        response = client.beta.messages.create(
            model=sampling_options["model"],
            messages=messages,
            system=[system_prompt],
            max_tokens=sampling_options["max_tokens"],
            tools=computer.list_tools(),
            betas=["computer-use-2024-10-22"],
        )

        # Store results from any tools Claude uses
        tool_results: list[BetaToolResultBlockParam] = []

        async def handle_tool_result(block: BetaToolUseBlockParam) -> None:
            """Handles execution of a single tool use request from Claude"""
            nonlocal tool_results
            # Validate the tool request
            try:
                action = Action(tool=block.name, params=block.input)
            except Exception:
                result = ToolResult(error=f"Tool {block.name} is invalid", output=None, base64_image=None, system=None)
                error_result = make_tool_result(result, block.id)
                logger.debug({"tool_use_error": error_result}, "Could not parse tool use")
                tool_results.append(error_result)  # noqa: B023
                return

            # Log the parsed action for debugging
            logger.debug(action.json(), "Parsed action:")

            # Execute the tool request and store result
            computer_response = await computer.execute(action)
            result = computer_response.tool_result
            if result:
                tool_result = make_tool_result(result, block.id)
                tool_results.append(tool_result)  # noqa: B023

        # Process Claude's response content sequentially
        assistant_content: list[BetaContentBlock] = []
        for content in response.content:
            assistant_content.append(content)
            if content.type == "text":  # type: ignore  # noqa: PGH003
                # Log Claude's text responses
                logger.info(f"Assistant: {content.text}")  # type: ignore  # noqa: PGH003
            elif content.type == "tool_use":  # type: ignore  # noqa: PGH003
                # Execute and log tool usage
                logger.info(f"Executing: {content.model_dump()}")
                await handle_tool_result(content)

        # Add Claude's response to conversation history
        messages.append({"role": "assistant", "content": assistant_content})

        # If tools were used, add results to conversation
        # Otherwise end the conversation loop
        if tool_results:
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    # Clean up and log completion
    logger.info(f"Completed task: {task}")
