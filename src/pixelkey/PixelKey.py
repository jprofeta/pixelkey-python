import re
from typing import Any, Union
from serial import Serial

from pixelkey import PixelKeyError, ErrorCode

class PixelKey:
    """PixelKey Controller API"""

    _nak_pattern = re.compile(r'^(?P<code>\d+) NAK$')
    _version_pattern = re.compile(r'^PixelKey v(?P<version>.+)$')

    def __init__(self, port:'str'):
        self.__serial = Serial(None, rtscts=False, xonxoff=False, dsrdtr=False)
        # Make sure the control lines are not asserted to keep the PixelKey from
        # thinking this is a terminal connection.
        self.__serial.rts = False
        self.__serial.dtr = False

        # Set the port and open it.
        self.__serial.port = port
        self.__serial.open()

        # Flush the input buffer just in case something was there or the control
        # lines glitched.
        self.__serial.reset_input_buffer()

        # Get the version of the attached PixelKey to make sure this is the
        # correct device.
        status = self.execute('$status')
        m = PixelKey._version_pattern.match(status)
        if m is None:
            self.__serial.close()
            raise PixelKeyError(ErrorCode.NONE, 'Status check failed.')
        self.__version = m.group('version')

    @property
    def is_open(self)->'bool':
        """Gets the state of the serial port."""
        return self.__serial.is_open

    @property
    def version(self)->'str':
        """Gets the firmware version of the attached PixelKey."""
        return self.__version

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def execute(self, cmd_str:'str') -> 'str | None':
        """Executes a command string."""
        self.__serial.write(cmd_str.encode(encoding="ascii") + b'\n')
        response = self.__serial.read_until().decode(encoding="ascii")

        if (nak := PixelKey._nak_pattern.match(response)) is not None:
            raise PixelKeyError(ErrorCode(int(nak.group('code'))))

        if response.startswith('OK'):
            return None
        
        rest = self.__serial.read_until('OK\n').decode(encoding="ascii")
        response += rest[:-3]   # Remove the OK\n from the response

        return response.strip()

    def close(self):
        """Close the internal serial port."""
        self.__serial.close()

    def config_set(self, key:'str', value:'Union[int,float,bool]'):
        """Set a configuration value for the attached PixelKey.
        
        Arguments:
            key: configuration option to set.
            value: value to set.
        """
        if not isinstance(key, str):
            raise TypeError('key must be a string')
        if not isinstance(value, int) and not isinstance(value, float) and not isinstance(value, bool):
            raise TypeError('value must be either an int, float, or bool.')

        self.execute(f'$config-set {key} {value}')

    def config_get(self, key:'str')->'Union[int,float,bool]':
        """Gets a configuration value from the attached PixelKey.
        
        Arguments:
            key: configuration option to get.

        Return:
            configuration value.
        """
        if not isinstance(key, str):
            raise TypeError('key must be a string')
        
        value = self.execute(f'$config-get {key}').lower()
        if value == 'true':
            return True
        if value == 'false':
            return False
        if value.isnumeric():
            return int(value, 0)
        try:
            return float(value)
        except:
            raise ValueError('Invalid configuration value type.')

