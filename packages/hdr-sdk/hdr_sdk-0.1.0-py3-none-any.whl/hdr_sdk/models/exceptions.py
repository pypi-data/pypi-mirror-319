class ComputerError(Exception):
    """Error raised when interacting with the remotecomputer."""

    pass


class ComputerToolError(Exception):
    """Error raised when interacting with the remotecomputer."""

    pass


class ToolCombineError(Exception):
    """Cannot combine tool results."""

    pass


class ToolError(Exception):
    """Raised when a tool encounters an error."""

    def __init__(self, message):
        self.message = message
