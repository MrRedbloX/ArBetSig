from pandas import DataFrame
from asyncio import get_event_loop as gel
from pyppeteer import launch
from bs4 import BeautifulSoup as bs

try:
    from config import config as cfg
except:
    from py.config import config as cfg

async def get_odds_from():
    def event_title(html):
        title = ""
        for sub_title in html.find('div', {'class': 'MatchDetails'}).find('a',{'class': 'MatchTitleLink'}).find('span').findAll('span'):
            title += sub_title.text
        title = title.replace('\xa0', ' ')
        return f"{title}|"

    def event_details(html):
        details = ""
        for detail in html.find('div', {'class': 'MatchDetails'}).find('div', {'class': 'BreadcrumbsLinks'}).find('ul', {'class': 'BreadMenu'}).findAll('li'):
            details += f"{details_text(detail)} - "
        return details

    def odd_class_text(html):
        return html.find('a').find('span', {'class': 'Odds'}).findAll('span')[-1].text

    def details_text(html):
        return html.find('a').find('span').text

    def clean_event(text):
        return text[0:len(event)-3]  #Removing last "-"

    def odds_type(html):
        return tuple(html.find('div', {'class': 'BetType'}).find('ol').findAll('li'))

    def odd_draw_text(html):
        return 0 if 'BookieDisabled' in html.span['class'] else odd_class_text(draw)

    def bookie_name(html):
        return html.find('a').find('span', {'class': 'BookieLogo BL'}).text

    browser = await launch()
    page = await browser.newPage()
    await page.goto(cfg['website'])
    await page.waitForSelector('ul.MatchesList')
    raw = await page.querySelectorEval('ul.MatchesList', '(elt) => elt.outerHTML')
    await browser.close()
    soup = bs(raw, features='lxml')
    matches = []
    for match in soup.find('ul', {'class': 'MatchesList'}):
        try:
            event = event_title(match)
            event += event_details(match)
            home, draw, away = odds_type(match)
            odd_draw = odd_draw_text(draw)
            matches.append(f"{clean_event(event)}&&{odd_class_text(home)}&&{bookie_name(home)}&&{odd_class_text(away)}&&{bookie_name(away)}&&{odd_draw}&&{None if odd_draw == 0 else bookie_name(draw)}")
        except:
            continue
    return matches

def get_odds_data():
    matches = gel().run_until_complete(get_odds_from())
    event_title_data = []
    event_details_data = []
    odd_home_data = []
    bookie_home_data = []
    odd_away_data = []
    bookie_away_data = []
    odd_draw_data = []
    bookie_draw_data = []
    for match in matches:
        event,odd_home,bookie_home,odd_away,bookie_away,odd_draw,bookie_draw = tuple(match.split('&&'))
        title, details = tuple(event.split('|'))
        event_title_data.append(title)
        event_details_data.append(details)
        odd_home_data.append(float(odd_home))
        bookie_home_data.append(bookie_home)
        odd_away_data.append(float(odd_away))
        bookie_away_data.append(bookie_away)
        odd_draw_data.append(float(odd_draw))
        bookie_draw_data.append(bookie_draw)
    data = {'Title': event_title_data, 'Details': event_details_data, 'Home': odd_home_data, 'Bookie Home': bookie_home_data, 'Away': odd_away_data, 'Bookie Away': bookie_away_data, 'Draw': odd_draw_data, 'Bookie Draw': bookie_draw_data}
    return DataFrame(data=data)

if __name__ == '__main__':
    print(get_odds_data())
