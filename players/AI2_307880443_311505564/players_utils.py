from __future__ import division, print_function
from utils import  INFINITY
import copy
from gameconsts import *

def is_calm_gen(player, max_deep):
    def is_calm(state, depth):
        moves = state.get_possible_moves()
        
        player.sd_depth = min(player.sd_depth, depth)  # for statistic purposes
        
        # if max depth or no moves, we are calm
        if abs(depth) >= max_deep or not moves:
            return True, moves
        
        # if the first move (and all the rest) are not conquering, we are calm
        if len(moves[0]) == 2:
            return True, moves
        
        # else we check to see if there's a move where we liberate our stack. if so this is not calm.
        for move in moves:
            if len(state.board[move[1]]) > 2 and state.board[move[1]][0].lower() != state.board[move[1]][1].lower():
                return False, moves 
        return True, moves   
    return is_calm

def our_utility_gen(player):
    POINT_PER_CAPTIVE = 1
    POINT_PER_SOLDER_STACK = 1
    POINT_PER_OFFICER_STACK = 2
    
    def utility(state):
        if not state.get_possible_moves():
            return INFINITY if state.curr_player != player.color else -INFINITY

        u = 0
        for square in state.board:
            if square[:1] in MY_COLORS[player.color]:
                # This tower belongs to me
                for piece in square:
                    if piece in OPPONENT_COLORS[player.color]:
                        # This piece is captured by me
                        u += POINT_PER_CAPTIVE
                u += POINT_PER_SOLDER_STACK if square[0] in SOLDIER_COLOR[player.color] else POINT_PER_OFFICER_STACK

            if square[:1] in OPPONENT_COLORS[player.color]:
                # This tower belongs to the opponent
                for piece in square:
                    if piece in MY_COLORS[player.color]:
                        # This piece is captured by the opponent
                        u -= POINT_PER_CAPTIVE
                u -= POINT_PER_SOLDER_STACK if square[0] in SOLDIER_COLOR[player.other_color] else POINT_PER_OFFICER_STACK

        return u
    return utility

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
