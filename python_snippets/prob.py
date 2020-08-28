import time
from html.parser import HTMLParser
from urllib.parse import urlsplit, urljoin
from urllib.request import urlopen

import requests

from extractor import LinkExtractor
from utils import time_track

sites = [
    'https://www.fl.ru',
    'https://www.weblancer.net/',
    'https://www.freelancejob.ru/',
    'https://kwork.ru',
]


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция работала {elapsed} секунд(ы)')
        return result
    return surrogate




class LinkExtractoR(HTMLParser):
    
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag not in ('link', 'script'):
            return
        attrs = dict(attrs)
        if tag == 'link':
            if 'rel' in attrs and attrs['rel'] == 'stylesheet':
                link = self._refine(attrs['href'])
                self.links.append(link)
        elif tag == 'script':
            if 'src' in attrs:
                link = self._refine(attrs['src'])
                self.links.append(link)

    def _refine(self, link):
        return urljoin(self.base_url,link)

class PageSizer:

    def __init__(self, url):
        self.url = url
        self.total_bytes = 0

    def run(self):
        self.total_bytes = 0
        html_data = self._get_html(url=self.url)
        if html_data is None:
            return

        self.total_bytes += len(html_data)
        extractor = LinkExtractoR(base_url=self.url)
        extractor.feed(html_data)
        for link in extractor.links:
            extra_data = self._get_html(url=link)
            if extra_data:
                self.total_bytes += len(extra_data)

    def _get_html(self, url):
        try:
            print(f'Go {url}......')
            res = requests.get(url)
        except Exception as exc:
            print(exc)
        else:
            return res.text


@time_track
def main():
    sizers = [PageSizer(url = url) for url in sites]

    for sizer in sizers:
        sizer.run()
    for sizer in sizers:
        print(f'for url {sizer.url} need download {sizer.total_bytes} bytes')

if __name__ == '__main__':
    main()


from collections import defaultdict

folder_in = 'trades'
ticker_dict = defaultdict(list)
ticker_volatility = []
ticker_volatility_zero = []

for dirpath, dirnames, filenames in os.walk(folder_in):
    for file in filenames:
        path = os.path.join(dirpath, file)

        with open(path, mode='r') as f:
            for line in f:
                secid, tradetime, price, quantity = line.split(',')
                if secid == "SECID":
                    continue

                ticker_dict[secid].append(float(price))


# Например для бумаги №1:
#   average_price = (12 + 11) / 2 = 11.5
#   volatility = ((12 - 11) / average_price) * 100 = 8.7%
# Для бумаги №2:
# print(ticker_dict['AFH9'])


for ticker in ticker_dict:
    average_price = (max(ticker_dict[ticker])+min(ticker_dict[ticker]))/2
    volatility = round(100*(max(ticker_dict[ticker])-min(ticker_dict[ticker]))/average_price,2)
    if volatility == 0:
        ticker_volatility_zero.append((ticker, volatility))
        continue
    ticker_volatility.append((ticker,volatility))
ticker_volatility.sort(key=lambda i: i[1], reverse=True)
ticker_volatility_zero.sort()


print('Максимальная волатильность')
for ticker in ticker_volatility[:3]:
    print(f'{ticker[0]} - {ticker[1]}%')

print('Минимальная волатильность')
for ticker in ticker_volatility[-3:]:
    print(f'{ticker[0]} - {ticker[1]}%')

print('Нулевая волатильность')
for ticker in ticker_volatility_zero:
    print(ticker[0])
