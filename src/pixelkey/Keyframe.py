
from typing import Optional

class Keyframe:
    """Base class for keyframes."""

    def __init__(self, name:'str', index_list:'Optional[list[int]]'=None, repeat_count:'Optional[int]'=None):
        if not isinstance(name, str):
            raise TypeError('name must be a str.')
        if index_list is not None and not isinstance(index_list, list):
            raise TypeError('index_list must be a list of int.')
        if repeat_count is not None and not isinstance(repeat_count, int):
            raise TypeError('count must be None or int.')

        if index_list is not None and (len(index_list) == 0 or not all(isinstance(x, int) or isinstance(x,tuple) for x in index_list)):
            raise ValueError('index_list must include at least one element and must be all ints')

        self.__name = name
        self.__index_list = index_list
        self.__repeat_count = repeat_count

    @property
    def name(self)->'str':
        """Gets the keyframe name used in the command string."""
        return self.__name

    @property
    def index_list(self)->'Optional[list[int]]':
        """Gets the NeoPixel index list to which apply this keyframe."""
        return self.__index_list

    @index_list.setter
    def index_list(self, index:'Optional[list[int]]'):
        if index is not None and not isinstance(index, list):
            raise TypeError('index_list must be a list of int.')
        if len(index) == 0 or not all(isinstance(x, int) or isinstance(x,tuple) for x in index):
            raise ValueError('index_list must include at least one element and must be all ints')
        self.__index_list = index

    @property
    def repeat_count(self)->'Optional[int]':
        """Get the number of repeats for this keyframe."""
        return self.__repeat_count

    @repeat_count.setter
    def repeat_count(self, count:'Optional[int]'):
        """Set the repeat count for this keyframe."""
        if count is not None and not isinstance(count, int):
            raise TypeError('count must be None or int.')
        self.__repeat_count = count

    def _get_argument_string(self)->'str':
        """Gets the argument string for a child keyframe."""
        raise NotImplementedError()

    def get_command(self)->'str':
        """Gets the command representation of this keyframe."""
        cmd_str = ''

        # Apply the keyframe modifiers
        if self.repeat_count is not None:
            cmd_str += f'^{self.repeat_count} '

        # Add the index list if provided
        if self.index_list is not None:
            cmd_str += ','.join(str(x) if isinstance(x,int) else str(x[0]) + '-' + str(x[1]) for x in self.index_list) + ' '

        # Build the rest of the command
        cmd_str += f'{self.name} {self._get_argument_string()}'

        return cmd_str

