import sys

def odds(win, loose, draw):
    if win == 0 or loose == 0:
        return 0
    return (1 / win + 1 / loose + (0 if draw == 0 else 1 / draw)) * 100

def fraction_to_decimal(frac):
    nume, deno = tuple(frac.split('/'))
    return float(nume) / float(deno) + 1

def from_fraction(win, loose, draw):
    return odds(fraction_to_decimal(win), fraction_to_decimal(loose), fraction_to_decimal(draw))

def compute_margin(win, loose, draw, mode):
    if mode == 'fraction':
        return from_fraction(win, loose, '-1/1' if draw == '0' else draw)
    elif mode == 'decimal':
        return odds(float(win), float(loose), float(draw))
    else:
        raise Exception("Unhandled mode in compute_margin function of odds.py module.")
        
if __name__ == "__main__":
    mode, win, loose, draw = (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    res = compute_margin(win, loose, draw, mode)
    print(f"Bookmaker is making {(res - 100):.2f} % of your bet no matter what.")
