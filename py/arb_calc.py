import sys

def stake_per_odd(home, away, draw, bet):
    margin = (1 / home + 1 / away + (0 if draw == 0 else 1 / draw))
    home_stake = bet * (1 / home) / margin
    away_stake = bet * (1 / away) / margin
    draw_stake = 0 if draw == 0 else bet * (1 / draw) / margin
    return [home_stake, away_stake, draw_stake]

if __name__ == '__main__':
    print(stake_per_odd(float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])))
