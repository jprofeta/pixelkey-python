import re
import time
from typing import Any, Union
from serial import Serial

from pixelkey import PixelKeyError, ErrorCode, Keyframe

class PixelKey:
    """PixelKey Controller API"""

    _version_pattern = re.compile(r'^PixelKey v(?P<version>.+).*')

    def __init__(self, port:'str'):
        self.__serial = Serial(None, timeout=0, rtscts=False, xonxoff=False, dsrdtr=False)
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
        self.__firmware_version = m.group('version')

    @property
    def is_open(self)->'bool':
        """Gets the state of the serial port."""
        return self.__serial.is_open

    @property
    def firmware_version(self)->'str':
        """Gets the firmware version of the attached PixelKey."""
        return self.__firmware_version

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def close(self):
        """Close the internal serial port."""
        self.__serial.close()

    def execute(self, cmd_str:'str') -> 'str | None':
        """Executes a command string."""
        self.__serial.write(cmd_str.encode(encoding="ascii") + b'\n')
        
        # Read until NAK or OK
        response = b''
        timeout = time.monotonic_ns() + 250000000   # 250 ms timeout
        while time.monotonic_ns() < timeout:
            if self.__serial.in_waiting > 0:
                response += self.__serial.read()
                # Check for the end of the response
                if response[-1] == b'\n'[0]:
                    line_start = response.rfind(b'\n', 0, -1)
                    if line_start == -1:
                        line_start = 0

                    if response.endswith(b' NAK\n'):
                        raise PixelKeyError(ErrorCode(int(response[line_start:-5]))) # Ignore ' NAK\n' at the end
                    elif response.endswith(b'OK\n'):
                        return response[:line_start].decode(encoding='ascii')
        raise TimeoutError()

    def push_keyframe(self, keyframe:'Keyframe'):
        """Pushes a keyframe to the PixelKey."""
        self.execute(keyframe.get_command())

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

