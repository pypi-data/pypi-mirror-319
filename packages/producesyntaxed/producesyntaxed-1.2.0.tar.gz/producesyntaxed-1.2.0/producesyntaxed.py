import sys

# Basic colors
RED = '\033[38;5;203m'
ORANGE = '\033[38;5;208m'
GREEN = '\033[38;5;120m'
YELLOW = '\033[38;5;226m'
BLUE = '\033[38;5;117m'  # dark-aqua sort of color
BLUE2 = '\033[96m'  # darker blue

# HTML color codes (in 256-color range for simplicity)
WHITE = '\033[38;5;15m'
BLACK = '\033[38;5;0m'
SILVER = '\033[38;5;7m'
GREY = '\033[38;5;8m'
MAROON = '\033[38;5;88m'
DARKRED = '\033[38;5;52m'
OLIVE = '\033[38;5;58m'
YELLOW2 = '\033[38;5;226m'
LIME = '\033[38;5;10m'
AQUA = '\033[38;5;14m'
TEAL = '\033[38;5;30m'
NAVY = '\033[38;5;17m'
FUCHSIA = '\033[38;5;13m'
PURPLE = '\033[38;5;5m'

# HTML-Color names to ANSI mapping
def producesyntaxed(text, color, useSpace=True, newLine=True):
    match color:
        case 'red':
            colour = RED
        case 'orange':
            colour = ORANGE
        case 'green':
            colour = GREEN
        case 'yellow':
            colour = YELLOW
        case 'blue':
            colour = BLUE
        case 'blue2':
            colour = BLUE2
        case 'white':
            colour = WHITE
        case 'black':
            colour = BLACK
        case 'silver':
            colour = SILVER
        case 'grey':
            colour = GREY
        case 'maroon':
            colour = MAROON
        case 'darkred':
            colour = DARKRED
        case 'olive':
            colour = OLIVE
        case 'lime':
            colour = LIME
        case 'aqua':
            colour = AQUA
        case 'teal':
            colour = TEAL
        case 'navy':
            colour = NAVY
        case 'fuchsia':
            colour = FUCHSIA
        case 'purple':
            colour = PURPLE
        case _:
            raise ValueError('Invalid color name')
    
    if useSpace and newLine:
        sys.stdout.write(colour + text + '\033[0m' + ' \n')
    elif useSpace:
        sys.stdout.write(colour + text + '\033[0m' + ' ')
    elif newLine:
        sys.stdout.write(colour + text + '\033[0m' + '\n')
    else:
        sys.stdout.write(colour + text + '\033[0m')

