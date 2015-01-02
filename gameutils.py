"""A game-specific implementations of utility functions.
"""
from __future__ import print_function, division
from gameconsts import *


class GameState:
    def __init__(self):
        """ Initializing the board and current player.
        """
        self.board = [
            BS, BS, BS, BS,
              BS, BS, BS,
            BS, BS, BS, BS,
              EM, EM, EM,
            WS, WS, WS, WS,
              WS, WS, WS,
            WS, WS, WS, WS
        ]
        self.curr_player = WHITE_PLAYER

    def calc_single_moves(self):
        """Calculating all the possible single moves.
        :return: All the legitimate single moves for this game state.
        """
        single_soldier_moves = [(i, j) for (i, j) in SOLDIER_SINGLE_MOVES[self.curr_player]
                                if self.board[i][:1] == SOLDIER_COLOR[self.curr_player]
                                and self.board[j] == EM]
        single_officer_moves = [(i, j) for (i, j) in OFFICER_SINGLE_MOVES
                                if self.board[i][:1] == OFFICER_COLOR[self.curr_player]
                                and self.board[j] == EM]
        return single_soldier_moves + single_officer_moves

    def calc_capture_moves(self):
        """Calculating all the possible capture moves, but only the first step.
        :return: All the legitimate single capture moves for this game state.
        """
        capture_soldier_moves = [(i, j, k) for (i, j, k) in SOLDIER_CAPTURE_MOVES[self.curr_player]
                                 if self.board[i][:1] == SOLDIER_COLOR[self.curr_player]
                                 and self.board[j][:1] in OPPONENT_COLORS[self.curr_player]
                                 and self.board[k][:1] == EM]
        capture_officer_moves = [(i, j, k) for (i, j, k) in OFFICER_CAPTURE_MOVES
                                 if self.board[i][:1] == OFFICER_COLOR[self.curr_player]
                                 and self.board[j][:1] in OPPONENT_COLORS[self.curr_player]
                                 and self.board[k][:1] == EM]
        return capture_soldier_moves + capture_officer_moves

    def find_following_moves(self, capture_move, move_privilege):
        """Given a capture move, return all long capture moves following this one. We do recursive DFS. We also don't
        replicate the board, but use the same self.board to avoid replication time.
        :param capture_move: The first 3-tuple that represents the move.
        :param move_privilege: The list of possible moves for every starting square.
        """
        # Temporarily changing the board, simulating the move and checking if there are more to follow.
        floating_piece = self.board[capture_move[1]]
        self.board[capture_move[1]] = EM
        self.board[capture_move[2]] = self.board[capture_move[0]]
        self.board[capture_move[0]] = EM

        next_moves = [(i, j, k) for (i, j, k) in move_privilege[capture_move[2]]
                      if self.board[j][:1] in OPPONENT_COLORS[self.curr_player]
                      and self.board[k][:1] == EM]

        def return_back_pieces():
            # Returning the board to its previous state
            self.board[capture_move[1]] = floating_piece
            self.board[capture_move[0]] = self.board[capture_move[2]]
            self.board[capture_move[2]] = EM

        if not next_moves:
            # This was the final move in a series of moves
            return_back_pieces()
            return [capture_move]

        possible_next_moves = []
        for next_move in next_moves:
            for move in self.find_following_moves(next_move, move_privilege):
                possible_next_moves.append(capture_move + move[1:])

        return_back_pieces()
        return possible_next_moves

    def get_possible_moves(self):
        """Return a list of possible moves for this state. Each possible move is represented by a list of square
        numbers.
        """
        possible_capture_moves = self.calc_capture_moves()
        if possible_capture_moves:
            # There is at least one capture move. Let's DFS them!
            self_curr_player = self.curr_player
            next_moves = []
            for capture_move in possible_capture_moves:
                if self.board[capture_move[0]][:1] == SOLDIER_COLOR[self_curr_player]:
                    next_moves += self.find_following_moves(capture_move, SOLDIER_CAPTURE_MOVES_FROM[self_curr_player])
                else:
                    next_moves += self.find_following_moves(capture_move, OFFICER_CAPTURE_MOVES_FROM)

            return next_moves

        # There were no capture moves. We return the single moves.
        return self.calc_single_moves()

    def perform_move(self, move):
        # The first square is always empty after the move.
        piece = self.board[move[0]]
        self.board[move[0]] = EM

        if len(move) == 2:
            # Single move
            self.board[move[1]] = piece
            if piece[:1] == SOLDIER_COLOR[self.curr_player] and move[1] in LAST_LINE[self.curr_player]:
                self.board[move[1]] = OFFICER_COLOR[self.curr_player] + piece[1:]

        else:
            # Capture move
            for (i, j) in [(i, i + 1) for i in xrange(1, len(move), 2)]:
                # Iterating over the pairs of capture square and destination square.
                captured = self.board[move[i]]
                self.board[move[i]] = captured[1:]
                self.board[move[j]] = piece + captured[:1]
                piece = self.board[move[j]]
                self.board[move[i - 1]] = EM

                if move[j] in LAST_LINE[self.curr_player] and piece[:1] == SOLDIER_COLOR[self.curr_player]:
                    # Promoting to officer
                    self.board[move[j]] = OFFICER_COLOR[self.curr_player] + self.board[move[j]][1:]

        # Updating the current player.
        self.curr_player = WHITE_PLAYER if self.curr_player == BLACK_PLAYER else BLACK_PLAYER


def draw_state(game_state):
    import gui
    gui.draw_state(game_state, 'gui/game.png', 'gui/Helvetica.ttf')


def draw(game_state, verbose):
    """Output the state.
    :param game_state: The GameState object to output.
    :param verbose: 'n' for no draw, 'g' for GUI draw, 't' for terminal draw.
    """
    if verbose == 'n':
        return

    try:
        if verbose == 'g':
            draw_state(game_state)
            return
    except IOError:
        # Fall back to terminal draw
        pass

    max_len = max((len(piece) for piece in game_state.board))
    # This weird string will be used to format the board cells.
    format_str = '{{:2}}:{{:^{}}}'.format(max_len)

    # Drawing the board row by row.
    i = 0
    for row in xrange(7):
        out_str = ''
        for col in xrange(7):
            if (row + col) % 2 == 0:
                # It's a piece place.
                out_str += format_str.format(i, game_state.board[i])
                i += 1
            else:
                # It's an always empty place.
                out_str += ' ' * (max_len + 3)
        print(out_str)
    print('*' * (7 * (max_len + 3)))


if __name__ == '__main__':
    # Testing stuff.
    s = GameState()
    print(len(s.board))
    # print(DOWN_RIGHT_MOVES)
    print([i for i in UP_SINGLE_MOVES])
    pass
