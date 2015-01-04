import sys
import os.path
import run_game

players = ['simple_player', 'player1', 'player2', 'player3']
setup_time = 2
times = [2.5, 10, 40]
k = 5
max_turns = 100
verbose = 't'

results_dir = 'results'

def get_full_player_name(player):
    if player == 'simple_player':
        return player
    return 'AI2_307880443_311505564.' + player

def run_single_game(setup_time, time_per_k_turns, k, maximum_turns_allowed, verbose, white_player, black_player):
    stdout = sys.stdout
    with open(os.path.join(results_dir, str(time_per_k_turns) + "_" + white_player + "_" + black_player + ".txt"), 'w') as f:
        sys.stdout = f
        white_player = get_full_player_name(white_player)
        black_player = get_full_player_name(black_player)
        winner = run_game.GameRunner(setup_time, time_per_k_turns, k, maximum_turns_allowed, verbose, white_player, black_player).run()
    sys.stdout = stdout
    return winner
        

if __name__ == "__main__":
    for time in times:
        for p1 in players:
            for p2 in players:
                if p1 == p2:
                    continue
                
                start_str = 'Running Game: {} vs {} for {} seconds.'.format(p1, p2, time)
                with open(os.path.join(results_dir, 'all.txt'), 'a') as f:
                    f.write(start_str + "\n")
                print start_str
                
                winner = run_single_game(setup_time, time, k, max_turns, verbose, p1, p2)
                
                win_str = 'Game: {} vs {} for {} seconds. Winner: {}'.format(p1, p2, time, winner)
                with open(os.path.join(results_dir, 'all.txt'), 'a') as f:
                    f.write(win_str + "\n")
                print win_str
