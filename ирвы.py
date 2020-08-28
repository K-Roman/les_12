# -*- coding: utf-8 -*-


# Задача: вычислить 3 тикера с максимальной и 3 тикера с минимальной волатильностью в МНОГОПРОЦЕССНОМ стиле
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
# TODO Внимание! это задание можно выполнять только после зачета lesson_012/02_volatility_with_threads.py !!!
import multiprocessing
import os
from _multiprocessing import recv
from multiprocessing import Process, Pipe, Queue, Pool
from utils import time_track

folder_in = 'trades'


class TickerVolatility():

    def __init__(self, file):
        # super().__init__()
        self.file = file
        self.ticker_volatility = []
        self.price_list = []
        # self.conn = conn

    def run(self):
        # print(multiprocessing.current_process(),flush=True)
        print(f'процесс {multiprocessing.current_process()}  взялся за файл {self.file}', flush=True, end='\n')
        with open(self.file, mode='r') as f:
            # print(f'открываю файл {file}',flush=True,end='\n')
            for line in f:
                secid, tradetime, price, quantity = line.split(',')
                if secid == "SECID":
                    continue
                self.price_list.append(float(price))

        average_price = (max(self.price_list) + min(self.price_list)) / 2
        volatility = round(100 * (max(self.price_list) - min(self.price_list)) / average_price, 2)
        # print(f'добавляю данные {(secid, volatility)}  файла {self.file}', flush=True, end='\n')
        # self.conn.send((secid, volatility))
        return (secid, volatility)


@time_track
def main():
    for dirpath, dirnames, filenames in os.walk(folder_in):
        # parent_conn, child_conn = Pipe()
        vols = [TickerVolatility(os.path.join(dirpath, file)) for file in filenames]
        # pipes = [parent_conn for file in filenames]
        with Pool(processes=5) as pool:

            ticker_all = pool.map(TickerVolatility.run, vols)
            print(ticker_all)

            # a = []
            # a += [pool.map(conn.recv(), pipes) for conn in pipes]
            # global ticker_all
            # ticker_all += a

        # ticker_all.append(a for a in res)
        # print(ticker_all)

    # results = [pool.apply_async(calculate, t) for t in TASKS]
    # imap_it = pool.imap(calculatestar, TASKS)
    # imap_unordered_it = pool.imap_unordered(calculatestar, TASKS)

    # for i, vol in enumerate(vols):
    #     vol.start()
    #
    #     print(f'{vol} process id:', os.getppid())
    #
    # ticker_all = [conn.recv() for conn in pipes]
    #
    #
    # for vol in vols:
    #     vol.join()
    #

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
