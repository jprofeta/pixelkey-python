from typing import Optional,Union
from pixelkey import Keyframe

# [index] blink <period> [color 1[:<color 2>]] [duty cycle]
class BlinkKeyframe(Keyframe):

    def __init__(self, period:'Union[float,int]', color1=None, color2=None, duty_cycle:'Optional[int]'=None, index_list:'Optional[list[int]]'=None, repeat_count:'Optional[str]'=None):
        super().__init__('blink', index_list=index_list, repeat_count=repeat_count)

        if period is None or (not isinstance(period, float) and not isinstance(period, int)):
            raise TypeError('period must be not None and a float or int.')

        if duty_cycle is not None and not isinstance(duty_cycle, int):
            raise TypeError('duty_cycle must be int or None')
        if duty_cycle is not None and (duty_cycle < 0 or duty_cycle > 100):
            raise ValueError('duty_cycle must be between 0 and 100')

        self.__period = period
        self.__color1 = color1
        self.__color2 = color2
        self.__duty_cycle = duty_cycle

    @property
    def period(self)->'float':
        """Period of the blink keyframe."""
        return self.__period
    @period.setter
    def period(self, value:'Union[float,int]'):
        if value is None or (not isinstance(value, float) and not isinstance(value, int)):
            raise TypeError('period must be not None and a float or int.')
        self.__period = value

    @property
    def color1(self):
        return self.__color1
    @color1.setter
    def color1(self, value):
        self.__color1 = value

    @property
    def color2(self):
        return self.__color2
    @color2.setter
    def color2(self, value):
        self.__color2 = value

    @property
    def duty_cycle(self):
        return self.__duty_cycle
    @period.setter
    def duty_cycle(self, value:'Optional[int]'):
        if value is not None and not isinstance(value, int):
            raise TypeError('duty_cycle must be int or None')
        if value is not None and (value < 0 or value > 100):
            raise ValueError('duty_cycle must be between 0 and 100')
        self.__duty_cycle = value

    def _get_argument_string(self) -> str:
        arg_str = f'{self.period}'

        if self.color1 is not None:
            arg_str += f' {self.color1}'
        else:
            return arg_str

        if self.color2 is not None:
            arg_str += f':{self.color2}'
        else:
            return arg_str

        if self.duty_cycle is not None:
            arg_str += f' {self.duty_cycle}'

        return arg_str
