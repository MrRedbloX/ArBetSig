from requests import get as rget

try:
    from config import config as cfg
except:
    from py.config import config as cfg

def send(df, local):
    df.rename(lambda x: x.lower().replace(' ','_').replace('%','pct_'), axis='columns', inplace=True)
    # print(df)
    try:
        url = cfg['url_local'] if local else cfg['url']
        rget(f"{url}/update_bets", params={"app_id": cfg['app_id'], "bets": df.to_numpy().tolist()})
    except Exception as e:
        print(f"Cannot send df: {e}")
