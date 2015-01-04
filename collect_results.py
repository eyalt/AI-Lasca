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

if __name__ == "__main__":
    with open(os.path.join(results_dir, "all.txt")) as f:
        lines = f.read().split('\n')
    lines = [":".join(l.split(":")[1:]).strip() for l in lines if l.startswith("Game:")]
    winners = {t:{} for t in times}
    points = {t:{p:0 for p in players} for t in times}
    for line in lines:
        parts = line.split()
        p1 = parts[0]
        p2 = parts[2]
        time = float(parts[4])
        winner = parts[-1].strip(")").strip("'")
        winners[time][(p1, p2)] = winner
    for t in sorted(winners):
        print "Time:", t
#         print winners[t]
        print "\n".join([str((p1,p2,winners[t][p1,p2])) for p1,p2 in sorted(winners[t])])
        for p1,p2 in winners[t]:
            result = winners[t][p1,p2]
            if result == 'white':
                points[t][p1] += 1
            elif result == 'black':
                points[t][p2] += 1
            elif result == 'tie':
                points[t][p1] += 0.5
                points[t][p2] += 0.5
            else:
                raise NameError("Unkown result: " + result + " For game: " + t + " " + p1 + " " + p2)
        print "\n".join(["%s" % p + " : "+str(points[t][p]) for p in sorted(points[t])])
        print "=============================="