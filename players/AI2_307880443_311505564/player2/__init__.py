from __future__ import division, print_function
import abstract
from utils import INFINITY
from gameconsts import *
import time
import copy

from players.AI2_307880443_311505564.players_utils import *

MAX_DEEPENING = 20

class Player(abstract.AbstractPlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        abstract.AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)
        self.other_color = WHITE_PLAYER if self.color == BLACK_PLAYER else BLACK_PLAYER
        self.clock = time.clock()
        self.time_per_k_turns *= 0.99
        self.remaining_time = self.time_per_k_turns
        
#         self.value_dict= 

        # We are simply providing (time_per_k_turns / k) per turn.
        # Taking a spare 1% time for unfolding the AlphaBeta.
        self.turn = 0
        self.average_moves_num = 0

        self.time_per_move = self.time_per_k_turns / self.k

    def get_move(self, game_state, possible_moves):
        self.clock = time.clock()
        
        if len(possible_moves) == 1:
            return 0

        current_depth = 1
        prev_alpha = -INFINITY

        # Choosing an arbitrary move:
        best_move = possible_moves[0]

        # Iterative deepening until the time runs out.
        while True:
            self.sd_depth = 0
            self.utility_time = 0
            
            print('going to depth: {}, remaining time: {}, prev_alpha: {}, best_move: {}'.format(
                current_depth, self.time_per_move - (time.clock() - self.clock), prev_alpha, best_move))
            minimax = MiniMaxWithAlphaBetaPruning_SD(self.utility, self.color, self.no_more_time, is_calm_gen(self, MAX_DEEPENING))
            alpha, move = minimax.search(game_state, current_depth, -INFINITY, INFINITY, True)
            print('U time: {}, maximal selective depth: {}, Regular leaves: {}, Deep leaves: {}'.format("%.3f" % self.utility_time, abs(self.sd_depth), minimax.reg_leaves, minimax.deep_leaves))
            
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
        if not state.get_possible_moves():
            return INFINITY if state.curr_player != self.color else -INFINITY

        u = 0
        for square in state.board:
            if square[:1] in MY_COLORS[self.color]:
                # This tower belongs to me
                for piece in square:
                    if piece in OPPONENT_COLORS[self.color]:
                        # This piece is captured by me
                        u += 1

            if square[:1] in OPPONENT_COLORS[self.color]:
                # This tower belongs to the opponent
                for piece in square:
                    if piece in MY_COLORS[self.color]:
                        # This piece is captured by the opponent
                        u -= 1

        return u
        
        self.utility_time += time.clock()
        return u

    def no_more_time(self):
        return (time.clock() - self.clock) >= self.time_per_move

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'Infected Beaver')




