from __future__ import division, print_function
import abstract
from utils import MiniMaxWithAlphaBetaPruning, INFINITY
from gameconsts import *
import time
import copy

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

    def is_calm(self, state, depth):
        moves = state.get_possible_moves()
        
        self.sd_depth = min(self.sd_depth, depth) # for statistic purposes
        
        # if max depth or no moves, we are calm
        if abs(depth) >= MAX_DEEPENING or not moves:
            return True, moves
        
        # if the first move (and all the rest) are not conquering, we are calm
        if len(moves[0]) == 2:
            return True, moves
        
        # else we check to see if there's a move where we liberate our stack. if so this is not calm.
        for move in moves:
            if len(state.board[move[1]]) > 2 and state.board[move[1]][0].lower() != state.board[move[1]][1].lower():
                return False, moves 
        return True, moves    
#         return False, moves

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'Infected Beaver')



# A class to handle the deepening until things are quiet
class MiniMaxWithAlphaBetaPruning_SD:

    def __init__(self, utility, my_color, no_more_time, is_calm):
        """Initialize a MiniMax algorithms with alpha-beta pruning.

        :param utility: The utility function. Should have state as parameter.
        :param my_color: The color of the player who runs this MiniMax search.
        :param no_more_time: A function that returns true if there is no more time to run this search, or false if
                             there is still time left.
        """
        self.utility = utility
        self.my_color = my_color
        self.no_more_time = no_more_time
        self.is_calm = is_calm
        
        self.reg_leaves = 0
        self.deep_leaves = 0

    def search(self, state, depth, alpha, beta, maximizing_player):
        """Start the MiniMax algorithm.

        :param state: The state to start from.
        :param depth: The maximum allowed depth for the algorithm.
        :param alpha: The alpha of the alpha-beta pruning.
        :param alpha: The beta of the alpha-beta pruning.
        :param maximizing_player: Whether this is a max node (True) or a min node (False).
        :return: A tuple: (The alpha-beta algorithm value, The move in case of max node or None in min mode)
        """
        
        if self.no_more_time():
            return self.utility(state), None
        
        next_moves = None
        self.reg_leaves += 1
        if depth <= 0:
            # statistic purposes
            if depth < 0:
                self.deep_leaves += 1
                self.reg_leaves -= 1
                
            # check if state is calm. if it is return its utility, else deepen into it
            calm, next_moves = self.is_calm(state, depth)
            if calm:
                return self.utility(state), None

        if next_moves is None:
            next_moves = state.get_possible_moves()
        if not next_moves:
            # This player has no moves. So the previous player is the winner.
            return INFINITY if state.curr_player != self.my_color else -INFINITY, None

        if maximizing_player:
            selected_move = next_moves[0]
            best_move_utility = -INFINITY
            for move in next_moves:
                new_state = copy.deepcopy(state)
                new_state.perform_move(move)
                minimax_value, _ = self.search(new_state, depth - 1, alpha, beta, False)
                alpha = max(alpha, minimax_value)
                if minimax_value > best_move_utility:
                    best_move_utility = minimax_value
                    selected_move = move
                if beta <= alpha or self.no_more_time():
                    break
            return alpha, selected_move

        else:
            for move in next_moves:
                new_state = copy.deepcopy(state)
                new_state.perform_move(move)
                beta = min(beta, self.search(new_state, depth - 1, alpha, beta, True)[0])
                if beta <= alpha or self.no_more_time():
                    break
            return beta, None
