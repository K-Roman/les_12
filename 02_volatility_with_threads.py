# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПОТОЧНОМ стиле
#
# Бумаги с нулевой волатильностью вывести отдельно.
# Результаты вывести на консоль в виде:
#   Максимальная волатильность:
#       ТИКЕР1 - ХХХ.ХХ %
#       ТИКЕР2 - ХХХ.ХХ %
#       ТИКЕР3 - ХХХ.ХХ %
#   Минимальная волатильность:
#       ТИКЕР4 - ХХХ.ХХ %
#       ТИКЕР5 - ХХХ.ХХ %
#       ТИКЕР6 - ХХХ.ХХ %
#   Нулевая волатильность:
#       ТИКЕР7, ТИКЕР8, ТИКЕР9, ТИКЕР10, ТИКЕР11, ТИКЕР12
# Волатильности указывать в порядке убывания. Тикеры с нулевой волатильностью упорядочить по имени.
#
# TODO Внимание! это задание можно выполнять только после зачета lesson_012/01_volatility.py !!!

# TODO тут ваш код в многопоточном стиле
import os
from threading import Thread
from utils import time_track
folder_in = 'trades'



class TickerVolatility(Thread):

    def __init__(self, file):
        super().__init__()
        self.file = file
        self.ticker_volatility = None
        self.price_list = []

    def run(self):
        secid = self.walk_dir(self.file, self.price_list)
        average_price = (max(self.price_list) + min(self.price_list)) / 2
        volatility = round(100 * (max(self.price_list) - min(self.price_list)) / average_price, 2)
        print(f'добавляю данные {(secid, volatility)}  файла {self.file}', flush=True, end='\n')
        self.ticker_volatility = (secid, volatility)
    # ticker_volatility.sort(key=lambda i: i[1], reverse=True)
    # ticker_volatility_zero.sort()

    def walk_dir(self, file, price_list):
        with open(file, mode='r') as f:
            print(f'открываю файл {file}',flush=True,end='\n')
            for line in f:
                secid, tradetime, price, quantity = line.split(',')
                if secid == "SECID":
                    continue
                price_list.append(float(price))
        return secid


@time_track
def main():
    for dirpath, dirnames, filenames in os.walk(folder_in):
        vols = [TickerVolatility(os.path.join(dirpath, file)) for file in filenames]
        print(vols)

    for vol in vols:
        vol.start()
    for vol in vols:
        vol.join()
    ticker_all = [vol.ticker_volatility for vol in vols]
    ticker_all.sort(key=lambda i: i[1], reverse=True)

    print('Максимальная волатильность')

    for ticker in ticker_all[:3]:
        print(f'{ticker[0]} - {ticker[1]}%')

    print('Минимальная волатильность')
    i = 0
    for ticker in ticker_all[::-1]:
        if ticker[1] != 0:
            i += 1
            print(f'{ticker[0]} - {ticker[1]}%')
            if i == 3:
                break

    print('Нулевая волатильность')
    for ticker in ticker_all:
        if ticker[1] == 0:
            print(f'{ticker[0]} - {ticker[1]}%')
# (vol.ticker_volatility[0], vol.ticker_volatility[1])
if __name__ == '__main__':
    main()



# print('Максимальная волатильность')
# for ticker in ticker1.ticker_volatility[:3]:
#     print(f'{ticker[0]} - {ticker[1]}%')
#
# print('Минимальная волатильность')
# for ticker in ticker1.ticker_volatility[-3:]:
#     print(f'{ticker[0]} - {ticker[1]}%')
#
# print('Нулевая волатильность')
# for ticker in ticker1.ticker_volatility_zero:
#     print(ticker[0])
