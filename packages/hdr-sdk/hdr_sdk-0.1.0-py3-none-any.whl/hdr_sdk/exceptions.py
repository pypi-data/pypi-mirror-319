class ComputerException(Exception):
    """Exception raised for errors in the computer connection"""

    pass


class ComputerNotConnected(ComputerException):
    """Client is not connected to a host computer"""

    pass


class ComputerTimeout(ComputerException):
    """Computer did not respond within the timeout"""

    pass
