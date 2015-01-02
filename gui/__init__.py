from __future__ import print_function
import Image
import ImageDraw
import ImageFont
from itertools import cycle
import gameutils
from gameconsts import *


SQUARE_COLORS = {
    WS: 'white',
    WO: 'green',
    BS: 'black',
    BO: 'red'
}


def draw_piece(draw, piece, bounding_square):
    for i, soldier in enumerate(reversed(piece)):
        draw.rectangle(
            map(lambda x, y: x + y,
                bounding_square,
                (10, 95 - (i + 1)*4, -10, -5 - (i + 1)*4 + 2)),
            fill=SQUARE_COLORS[soldier])


def draw_board(font, game_state):
    n = 7
    pixel_width = 700

    def sq_start(i):
        """Return the x/y start coord of the square at column/row i."""
        return i * pixel_width / n

    def square(i, j):
        """Return the square corners, suitable for use in PIL drawings"""
        return map(sq_start, [i, j, i + 1, j + 1])

    image = Image.new('RGB', (pixel_width, pixel_width), '#8e7555')
    draw = ImageDraw.Draw(image)
    squares = (square(i, j)
               for i_start, j in zip(cycle((0, 1)), range(n))
               for i in range(i_start, n, 2))
    for i, sq in enumerate(squares):
        draw.rectangle(sq, fill='#b6aa8c')
        draw.text(sq[:2], str(i), 'black', font)
        draw_piece(draw, game_state.board[i], sq)

    return image


def draw_state(game_state, out_file, font_file):
    font = ImageFont.truetype(font_file, 17)
    im = draw_board(font, game_state)
    im.save(out_file)
    raw_input('Press enter to continue')


if __name__ == '__main__':
    draw_state(gameutils.GameState(), 'test.png', 'Helvetica.ttf')