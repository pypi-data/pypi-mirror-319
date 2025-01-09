from collections import namedtuple
from enum import Enum

Color = namedtuple('Color', ['foreground_color', 'background_color'])

_WHITE = 'rgb(240, 240, 240)'
_DARK = 'rgb(50, 50, 50)'


class Colors(Enum):
    """buttons color themes."""

    DISABLED = Color('rgb(80, 80, 80)', 'rgb(180, 180, 180)')

    BLUE = Color('rgb(46, 134, 193)', _WHITE)
    RED = Color('rgb(160, 20, 20)', _WHITE)
    ORANGE = Color('rgb(236, 183, 41)', _WHITE)
    GREEN = Color('rgb(40, 205, 50)', _WHITE)
    YELLOW = Color('rgb(200, 200, 0)', _WHITE)
    GREY = Color('rgb(80, 80, 80)', _WHITE)
    WHITE = Color('rgb(30, 30, 30)', _WHITE)

    # dark theme
    DARK_BLUE = Color('rgb(46, 134, 193)', _DARK)
    DARK_RED = Color('rgb(200, 10, 10)', _DARK)
    DARK_ORANGE = Color('rgb(236, 183, 41)', _DARK)
    DARK_GREEN = Color('rgb(40, 205, 50)', _DARK)
    DARK_YELLOW = Color('rgb(240, 240, 0)', _DARK)
    DARK_GREY = Color('rgb(80, 80, 80)', _DARK)
    DARK_WHITE = Color('rgb(240, 240, 240)', _DARK)

    # full background color
    BG_BLUE = Color(_WHITE, 'rgb(46, 134, 193)')
    BG_RED = Color(_WHITE, 'rgb(160, 20, 20)')
    BG_ORANGE = Color(_DARK, 'rgb(236, 183, 41)')
    BG_GREEN = Color(_WHITE, 'rgb(40, 205, 50)')
    BG_YELLOW = Color(_DARK, 'rgb(220, 220, 0)')
    BG_GREY = Color(_WHITE, 'rgb(80, 80, 80)')
    BG_WHITE = Color(_DARK, _WHITE)
    BG_BLACK = Color(_WHITE, 'rgb(30, 30, 30)')


if __name__ == '__main__':
    print(
        f'Value for {Colors.BLUE} is '
        f'foreground_color {Colors.BLUE.value.foreground_color} and '
        f'background_color {Colors.BLUE.value.background_color}'
    )
