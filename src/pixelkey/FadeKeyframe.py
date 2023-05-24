from typing import Optional, Union
from pixelkey import Keyframe

# [index] fade <period> [&]<color 1>[:<color 2>:...] [type]
class FadeKeyframe(Keyframe):

    def __init__(self, period:'Union[int,float]', color, fade_type=None, push_current_color=False, index_list:'Optional[list[int]]'=None, repeat_count:'Optional[str]'=None):
        super().__init__('fade', index_list=index_list, repeat_count=repeat_count)

        if period is None or (not isinstance(period, float) and not isinstance(period, int)):
            raise TypeError('period must be not None and a float or int.')

        self.__period = period
        self.__color = color
        self.__fade_type = fade_type
        self.__push_current_color = push_current_color

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
    def color(self)->'list':
        """Color list to fade across."""
        return self.__color
    @color.setter
    def color(self, value):
        self.__color = value

    @property
    def fade_type(self):
        """Type of fade to perform."""
        return self.__fade_type
    @fade_type.setter
    def fade_type(self, value):
        self.__fade_type = value

    @property
    def push_current_color(self)->'bool':
        """Push the current color as the first color to fade across."""
        return self.__push_current_color
    @push_current_color.setter
    def push_current_color(self, value:'bool'):
        if not isinstance(value, bool):
            raise TypeError('push_current_color must be a bool')
        self.__push_current_color = value

    def _get_argument_string(self) -> str:
        arg_str = f'{self.period} '

        if self.push_current_color:
            arg_str += '&'
        
        if isinstance(self.color,list):
            arg_str += ':'.join(self.color)
        else:
            arg_str += str(self.color)
        
        if self.fade_type is not None:
            arg_str += f' {self.fade_type}'

        return arg_str

