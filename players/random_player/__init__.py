import abstract
import random


class Player(abstract.AbstractPlayer):
    def __init__(self, setup_time, player_color, time_per_k_turns, k):
        abstract.AbstractPlayer.__init__(self, setup_time, player_color, time_per_k_turns, k)

    def get_move(self, game_state, possible_moves):
        return random.choice(range(len(possible_moves)))

    def __repr__(self):
        return '{} {}'.format(abstract.AbstractPlayer.__repr__(self), 'random')