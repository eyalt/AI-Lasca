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
        self.clock = time.clock()
        
        # We are simply providing (time_per_k_turns / k) per turn.
        # Taking a spare 1% time for unfolding the AlphaBeta.
        self.time_per_move = 0.99 * self.time_per_k_turns / self.k

        self.other_color = WHITE_PLAYER if self.color == BLACK_PLAYER else BLACK_PLAYER
        self.utility = our_utility_gen(self)
        self.is_calm = is_calm_gen(self, MAX_DEEPENING)

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
            minimax = MiniMaxWithAlphaBetaPruning_SD(self.utility, self.color, self.no_more_time, self.is_calm)
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

    def no_more_time(self):
        return (time.clock() - self.clock) >= self.time_per_move

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'Ultra Mega')




