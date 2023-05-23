from typing import Optional

from pixelkey import ErrorCode

class PixelKeyError(BaseException):
    """PixelKey error."""

    def __init__(self, error_code:'ErrorCode', message:'Optional[str]'=None):
        msg = f"NAK {error_code}"
        if message is not None:
            msg += f": {message}"
        super().__init__(msg)

        self._error_code = error_code
        self._message = message

    @property
    def error_code(self):
        """Get the error code returned by the PixelKey."""
        return self._error_code

    @property
    def message(self):
        """Get the message for this error."""
        return self._message
