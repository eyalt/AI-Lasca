from __future__ import division, print_function
import abstract
from utils import MiniMaxWithAlphaBetaPruning, INFINITY
from gameconsts import *
import time

SIDE_SQUARES = [0,3,7,10,14,17,21,24]
POINT_FOR_CAPTURED = 4
POINT_FOR_OFFICER = 5
POINT_FOR_EATING = 10
POINT_FOR_BASE = 1
POINT_FOR_SIDE = 1
POINT_FOR_DEFENDED = 1

class Player(abstract.AbstractPlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        abstract.AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.other_color = WHITE_PLAYER if self.color == BLACK_PLAYER else BLACK_PLAYER
        self.clock = time.clock()
        self.time_per_k_turns *= 0.99
        self.remaining_time = self.time_per_k_turns

        # We are simply providing (time_per_k_turns / k) per turn.
        # Taking a spare 1% time for unfolding the AlphaBeta.
        self.turn = 0
        self.average_moves_num = 0
        self.moves_till_now = 0

        self.time_per_move = self.time_per_k_turns / self.k

    def get_move(self, game_state, possible_moves):
        self.turn = (self.turn + 1) % self.k

        if self.moves_till_now == 0:
            self.average_moves_num = len(possible_moves)
        else:
            self.average_moves_num = (self.moves_till_now + 1)*(self.average_moves_num/float(self.moves_till_now) + len(possible_moves))
        
        self.moves_till_now = self.moves_till_now + 1
        self.move_time = self.calc_move_time(len(possible_moves))
        self.remaining_time = max(self.remaining_time - self.move_time,0)
        
        self.clock = time.clock()
        if len(possible_moves) == 1:
            return 0

        current_depth = 1
        prev_alpha = -INFINITY

        # Choosing an arbitrary move:
        best_move = possible_moves[0]

        # Iterative deepening until the time runs out.
        while True:
            print('going to depth: {}, remaining time: {}, prev_alpha: {}, best_move: {}'.format(
                current_depth, self.move_time - (time.clock() - self.clock), prev_alpha, best_move))
            minimax = MiniMaxWithAlphaBetaPruning(self.utility, self.color, self.no_more_time)
            alpha, move = minimax.search(game_state, current_depth, -INFINITY, INFINITY, True)

            if self.no_more_time():
                print('no more time')
                break

            prev_alpha = alpha
            best_move = move

            if alpha == INFINITY:
                print('the move: {} will guarantee victory.'.format(best_move))
                break

            current_depth += 1

        return possible_moves.index(best_move)

    def utility(self, state):
        possible_moves = state.get_possible_moves()
        if not possible_moves:
            return INFINITY if state.curr_player != self.color else -INFINITY

        u = 0

        
        for index,square in enumerate(state.board):

            # Difference in captured
            if square[:1] in MY_COLORS[self.color]:
                # This tower belongs to me
                for piece in square:
                    if piece in OPPONENT_COLORS[self.color]:
                        # This piece is captured by me
                        u += POINT_FOR_CAPTURED
            if square[:1] in OPPONENT_COLORS[self.color]:
                # This tower belongs to the opponent
                for piece in square:
                    if piece in MY_COLORS[self.color]:
                        # This piece is captured by the opponent
                        u -= POINT_FOR_CAPTURED

            # Difference in officers
            if square[:1]  == OFFICER_COLOR[self.color]:
                u += POINT_FOR_OFFICER
            if square[:1] in OFFICER_COLOR and square[:1] != OFFICER_COLOR[self.color]:
                u -= POINT_FOR_OFFICER

            # POSSIBLY BAD FEATURE
            # Number of defended tools
            if state.board[SOLDIER_SINGLE_MOVES[self.color][index][1]] in MY_COLORS[self.color]:
                u += POINT_FOR_DEFENDED
            if state.board[SOLDIER_SINGLE_MOVES[self.other_color][index][1]] in OPPONENT_COLORS[self.color]:
                u -= POINT_FOR_DEFENDED

        # POSSIBLY BAD FEATURE!
        # Protection of base
        if self.color == WHITE_PLAYER:
            u += POINT_FOR_BASE*len([x for x in state.board[:4] if x in MY_COLORS[self.color]])
            u -= POINT_FOR_BASE*len([x for x in state.board[-3:] if x in OPPONENT_COLORS[self.color]])
        else:
            u += POINT_FOR_SIDE*len([x for x in state.board[-3:] if x in MY_COLORS[self.color]])
            u -= POINT_FOR_SIDE*len([x for x in state.board[:4] if x in OPPONENT_COLORS[self.color]])

        # POSSIBLY BAD FEATURE!
        # Squares on sides
        for index in SIDE_SQUARES:
            if state.board[index] in MY_COLORS[self.color]:
                u -=POINT_FOR_SIDE
            if state.board[index] in OPPONENT_COLORS[self.color]:
                u +=POINT_FOR_SIDE

        # POSSIBLY BAD FEATURE!
        # How good is the next turn for the curr player
        if state.curr_player == self.color:
            u += POINT_FOR_EATING*len(state.calc_capture_moves())
        else:
            u -= POINT_FOR_EATING*len(state.calc_capture_moves())

        return u

    def no_more_time(self):
        return (time.clock() - self.clock) >= self.move_time

    def calc_move_time(self, moves_num):
        if self.turn % self.k == 0:
            return self.remaining_time
        if moves_num == 1:
            return 0
        return self.time_per_move
        # return self.time_per_k_turns*(moves_num - 1)/float(self.average_moves_num*self.k)

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'Infected Beaver')