from typing import Optional
from pixelkey import Keyframe

# [index] set <color>
class SetKeyframe(Keyframe):

    def __init__(self, color, index_list:'Optional[list[int]]'=None, repeat_count:'Optional[str]'=None):
        super().__init__('set', index_list=index_list, repeat_count=repeat_count)

        self.__color = color

    @property
    def color(self):
        """Get the color for this keyframe."""
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    def _get_argument_string(self) -> str:
        return str(self.color)
