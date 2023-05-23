from enum import Enum

class ErrorCode(Enum):
    """Error codes returned by the PixelKey."""
    NONE = 0
    INVALID_ARGUMENT = 1
    BUFFER_FULL = 2
    COMMUNICATION_ERROR = 3
    INPUT_BUFFER_OVERFLOW = 4
    INDEX_OUT_OF_RANGE = 5
    KEYFRAME_PROCESSING_STOPPED = 6
    RTC_NOT_SET = 7
    NOT_ENOUGH_ARGUMENTS = 8
    TOO_MANY_ARGUMENTS = 9
    UNKNOWN_COMMAND = 10
    KEY_NOT_FOUND = 16
    NV_MEMORY_ERROR = 17
    VALUE_OUT_OF_RANGE = 18
    NV_NOT_INITIALIZED = 19
    NV_CRC_MISMATCH = 20
    MISSING_BLOCKS = 32
    CRC_MISMATCH = 33
    OUT_OF_MEMORY = 48
    HAL_ERROR = 49

    def __repr__(self):
        return "%d (%s)" % (self.value, self._name_)
