"""A generic turn-based game runner.
"""
from __future__ import print_function
import sys
import gameutils
import utils
import copy
from gameconsts import WHITE_PLAYER, BLACK_PLAYER, TIE
import players.interactive


class GameRunner:
    def __init__(self, setup_time, time_per_k_turns, k, maximum_turns_allowed, verbose, white_player, black_player):
        """Game runner initialization.

        :param setup_time: Setup time allowed for each player in seconds. Can be a fraction or inf.
        :param time_per_k_turns: Time allowed per k moves in seconds. Can be a fraction or inf.
            The interactive player always gets infinite time to decide, no matter what.
        :param k: The k turns we measure time on. Must be a positive integer.
        :param maximum_turns_allowed: Maximum moves allowed per player. E.g. 50 means 100 moves, 50 white and 50 black
            moves. Can be an integer or inf.
        :param verbose: The level of verbosity of describing the progress of the game.
            One of the following: (n, t, g) for (no draw, terminal, gui) respectively.
        :param white_player: The name of the module containing the white player. E.g. "myplayer" will invoke an
            equivalent to "import players.myplayer" in the code.
        :param black_player: Same as 'white_player' parameter, but for the black one.
        """

        self.verbose = verbose.lower()
        self.setup_time = float(setup_time)
        self.time_per_k_turns = float(time_per_k_turns)
        self.k = int(k)
        self.maximum_turns_allowed = float(maximum_turns_allowed) if maximum_turns_allowed == 'inf' \
            else int(maximum_turns_allowed)

        self.players = []

        # Dynamically importing the players. This allows maximum flexibility and modularity.
        self.white_player = 'players.{}'.format(white_player)
        self.black_player = 'players.{}'.format(black_player)
        __import__(self.white_player)
        __import__(self.black_player)
        white_is_interactive = sys.modules[self.white_player].Player == players.interactive.Player
        black_is_interactive = sys.modules[self.black_player].Player == players.interactive.Player
        self.remaining_times = [
            utils.INFINITY if white_is_interactive else self.time_per_k_turns,
            utils.INFINITY if black_is_interactive else self.time_per_k_turns,
        ]

    def setup_player(self, player_class, player_color):
        """ An auxiliary function to populate the players list, and measure setup times on the go.

        :param player_class: The player class that should be initialized, measured and put into the list.
        :param player_color: Player color, passed as an argument to the player.
        :return: A boolean. True if the player exceeded the given time. False otherwise.
        """
        try:
            player, measured_time = utils.run_with_limited_time(
                player_class, (self.setup_time, player_color, self.time_per_k_turns, self.k), {}, self.setup_time)
        except MemoryError:
            return True

        self.players.append(player)
        return measured_time > self.setup_time

    def run(self):
        """The main loop.
        :return: The winner.
        """

        white_player_exceeded = self.setup_player(sys.modules[self.white_player].Player, WHITE_PLAYER)
        black_player_exceeded = self.setup_player(sys.modules[self.black_player].Player, BLACK_PLAYER)
        winner = self.handle_time_expired(white_player_exceeded, black_player_exceeded)
        if winner:
            return winner

        game_state = gameutils.GameState()
        curr_player_idx = 0

        remaining_run_times = self.remaining_times[:]
        k_count = 0
        turns_elapsed = 0

        # Running the actual game loop. The game ends if someone is left out of moves,
        # exceeds his time or maximum turns limit was reached.
        while True:
            gameutils.draw(game_state, self.verbose)

            player = self.players[curr_player_idx]
            remaining_run_time = remaining_run_times[curr_player_idx]
            try:
                possible_moves = game_state.get_possible_moves()
                self.print_if_verbose('Possible moves: {}'.format(possible_moves))
                if not possible_moves:
                    winner = self.make_winner_result(0 if curr_player_idx == 1 else 1)
                    break
                move_idx, run_time = utils.run_with_limited_time(
                    player.get_move, (copy.deepcopy(game_state), possible_moves), {}, remaining_run_time)
                remaining_run_times[curr_player_idx] -= run_time
                if remaining_run_times[curr_player_idx] < 0:
                    raise utils.ExceededTimeError
            except (utils.ExceededTimeError, MemoryError):
                self.print_if_verbose('Player {} exceeded resources.'.format(player))
                winner = self.make_winner_result(0 if curr_player_idx == 1 else 1)
                break

            game_state.perform_move(possible_moves[move_idx])
            self.print_if_verbose('Player ' + repr(player) + ' performed the move: ' + repr(possible_moves[move_idx]))
            curr_player_idx = (curr_player_idx + 1) % 2

            if curr_player_idx == 0:
                # White and black played.
                k_count = (k_count + 1) % self.k
                if k_count == 0:
                    # K rounds completed. Resetting timers.
                    remaining_run_times = self.remaining_times[:]

                turns_elapsed += 1
                if turns_elapsed == self.maximum_turns_allowed:
                    winner = self.make_winner_result(-1)
                    break

        self.end_game(winner, turns_elapsed)
        return winner

    @staticmethod
    def end_game(winner, turns_elapsed):
        print('The winner is {}, turns elapsed: {}'.format(winner[0], turns_elapsed))

    def make_winner_result(self, idx):
        if idx < 0:
            return TIE, TIE

        if idx == 0:
            return self.players[0], WHITE_PLAYER

        return self.players[1] if len(self.players) > 1 else BLACK_PLAYER, BLACK_PLAYER

    def handle_time_expired(self, white_player_exceeded, black_player_exceeded):
        winner = None
        if white_player_exceeded and black_player_exceeded:
            winner = self.make_winner_result(-1)
        elif white_player_exceeded:
            winner = self.make_winner_result(1)
        elif black_player_exceeded:
            winner = self.make_winner_result(0)

        if winner:
            self.end_game(winner, 0)

        return winner

    def print_if_verbose(self, out_str):
        if self.verbose in ('t', 'g'):
            print(out_str)

if __name__ == '__main__':
    try:
        GameRunner(*sys.argv[1:]).run()
    except TypeError:
        print("""Syntax: {0} setup_time time_per_k_turns k maximum_turns_allowed verbose white_player black_player
For example: {0} 3 3 3 50 g interactive simple_player
Please read the docs in the code for more info.""".
              format(sys.argv[0]))