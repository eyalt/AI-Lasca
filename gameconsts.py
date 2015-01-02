
# White and black soldiers and officers. Empty spaces.
WS = 'w'
WO = 'W'
BS = 'b'
BO = 'B'
EM = ''
WHITE_PLAYER = 'white'
BLACK_PLAYER = 'black'
TIE = 'tie'

# Generating the possible single moves. The weird 'if' is making sure we don't go out of board.
DOWN_RIGHT_SINGLE_MOVES = [(i, i + 4) for i in xrange(25) if i % 7 != 3 and i + 4 < 25]
DOWN_LEFT_SINGLE_MOVES = [(i, i + 3) for i in xrange(25) if i % 7 != 0 and i + 3 < 25]
UP_RIGHT_SINGLE_MOVES = [(j, i) for (i, j) in DOWN_LEFT_SINGLE_MOVES]
UP_LEFT_SINGLE_MOVES = [(j, i) for (i, j) in DOWN_RIGHT_SINGLE_MOVES]
UP_SINGLE_MOVES = UP_LEFT_SINGLE_MOVES + UP_RIGHT_SINGLE_MOVES
DOWN_SINGLE_MOVES = DOWN_LEFT_SINGLE_MOVES + DOWN_RIGHT_SINGLE_MOVES
OFFICER_SINGLE_MOVES = UP_SINGLE_MOVES + DOWN_SINGLE_MOVES


# Generating the possible capture moves. Paring single moves for this purpose.
def calc_capture_moves(single_moves):
    return [(i, j, k)
            for (i, j) in single_moves
            for (j2, k) in single_moves
            if j == j2]

DOWN_RIGHT_CAPTURE_MOVES = calc_capture_moves(DOWN_RIGHT_SINGLE_MOVES)
DOWN_LEFT_CAPTURE_MOVES = calc_capture_moves(DOWN_LEFT_SINGLE_MOVES)
UP_RIGHT_CAPTURE_MOVES = calc_capture_moves(UP_RIGHT_SINGLE_MOVES)
UP_LEFT_CAPTURE_MOVES = calc_capture_moves(UP_LEFT_SINGLE_MOVES)
UP_CAPTURE_MOVES = UP_LEFT_CAPTURE_MOVES + UP_RIGHT_CAPTURE_MOVES
DOWN_CAPTURE_MOVES = DOWN_LEFT_CAPTURE_MOVES + DOWN_RIGHT_CAPTURE_MOVES
OFFICER_CAPTURE_MOVES = UP_CAPTURE_MOVES + DOWN_CAPTURE_MOVES


# Assigning moves to specific players
SOLDIER_SINGLE_MOVES = {
    WHITE_PLAYER: UP_SINGLE_MOVES,
    BLACK_PLAYER: DOWN_SINGLE_MOVES,
}
SOLDIER_CAPTURE_MOVES = {
    WHITE_PLAYER: UP_CAPTURE_MOVES,
    BLACK_PLAYER: DOWN_CAPTURE_MOVES,
}

# Assigning colors
SOLDIER_COLOR = {
    WHITE_PLAYER: WS,
    BLACK_PLAYER: BS,
}
OFFICER_COLOR = {
    WHITE_PLAYER: WO,
    BLACK_PLAYER: BO,
}
MY_COLORS = {
    WHITE_PLAYER: (WS, WO),
    BLACK_PLAYER: (BS, BO)
}
OPPONENT_COLORS = {
    WHITE_PLAYER: (BS, BO),
    BLACK_PLAYER: (WS, WO),
}

# Last lines of board
LAST_LINE = {
    WHITE_PLAYER: (0, 1, 2, 3),
    BLACK_PLAYER: (21, 22, 23, 24),
}

# Pre-calculation capture moves from each square to avoid calculating it over and over again
# in the DFS of capture moves

OFFICER_CAPTURE_MOVES_FROM = []
for i in range(25):
    OFFICER_CAPTURE_MOVES_FROM.append([capture_move for capture_move in OFFICER_CAPTURE_MOVES
                                       if capture_move[0] == i])

SOLDIER_CAPTURE_MOVES_FROM = {
    WHITE_PLAYER: [],
    BLACK_PLAYER: [],
}

for player, moves in zip((WHITE_PLAYER, BLACK_PLAYER), (UP_CAPTURE_MOVES, DOWN_CAPTURE_MOVES)):
    for i in range(25):
        SOLDIER_CAPTURE_MOVES_FROM[player].append([capture_move for capture_move in moves
                                                   if capture_move[0] == i])

