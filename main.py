import sys
from numpy import array as npa
from numpy import around
from time import sleep
from gc import collect

from py.odds import compute_margin
from py.data import get_odds_data
from py.arb_calc import stake_per_odd
from py.sender import send

def main(local):
    while True:
        try:
            df = get_odds_data()
            df['%Odds'] = df.apply(lambda x: compute_margin(x['Home'], x['Away'], x['Draw'], 'decimal') - 100, axis=1)
            df.drop(df[df['%Odds'] >= 0].index, inplace=True)
            if not df.empty:
                df['%Stake'] = df.apply(lambda x: around((npa(stake_per_odd(x['Home'], x['Away'], x['Draw'], 100)) / 100).tolist(), decimals=2), axis=1)
                df = df.round({'%Stake': 2, '%Odds': 2})
                send(df.reset_index().drop(columns='index', axis=1), local)
        except Exception as e:
            print(e)
        sleep(2)
        collect()

if __name__ == '__main__':
    main(True if len(sys.argv) > 1 else False)

# TODO: Relook at stake per odd computation
# TODO: Build a basic web servive to display data
