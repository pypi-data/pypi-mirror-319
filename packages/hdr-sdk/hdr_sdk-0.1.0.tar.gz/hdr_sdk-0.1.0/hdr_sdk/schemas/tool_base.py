from dataclasses import dataclass, fields, replace

from hdr_sdk.models.exceptions import ToolCombineError


@dataclass(kw_only=True, frozen=True)
class ToolResult:
    """Result from executing a tool command.

    Contains the command output, any errors, base64 encoded screenshots,
    and system messages.
    """

    output: str | dict | None = None
    error: str | None = None
    base64_image: str | None = None
    system: str | None = None

    def __bool__(self) -> bool:
        """Returns True if any field has a non-None value."""
        return any(getattr(self, field.name) for field in fields(self))

    def __add__(self, other: "ToolResult") -> "ToolResult":
        """Combines two ToolResults.

        String fields are concatenated, base64_image cannot be combined.
        Returns a new ToolResult with combined fields.

        Raises:
            ToolCombineError: If base64_image fields conflict
        """

        def combine_fields(field: str | None, other_field: str | None, concatenate: bool = True) -> str | None:
            if field and other_field:
                if concatenate:
                    return field + other_field
                raise ToolCombineError("Cannot combine tool results")  # noqa: TRY003
            return field or other_field

        return ToolResult(
            output=combine_fields(self.output, other.output),
            error=combine_fields(self.error, other.error),
            base64_image=combine_fields(self.base64_image, other.base64_image, False),
            system=combine_fields(self.system, other.system),
        )

    def replace(self, **kwargs) -> "ToolResult":
        """Returns a new ToolResult with the given fields replaced."""
        return replace(self, **kwargs)


class CLIResult(ToolResult):
    """A ToolResult that can be rendered as a CLI output."""


class ToolFailure(ToolResult):
    """A ToolResult that represents a failure."""
