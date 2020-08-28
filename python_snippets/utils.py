import time


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()

        result = func(*args, **kwargs)

        ended_at = time.time()
        elapsed = round(ended_at - started_at, 4)
        print(f'Функция работала {elapsed} секунд(ы)')
        return result
    return surrogate



class VolDataProcessor:

    def __init__(self, vols_container):
        self.max = []
        self.min = []
        self.zero = []
        self.vols_container = vols_container

    # что-то мне подсказывает, что такое использование специального метода
    # не совсем корректно...если так, жду замечания)
    def __str__(self):
        self.print_values()
        return '-'

    def construct_zero(self):
        while True:
            if self.vols_container[-1]['volatility'] == 0:
                self.zero.append(self.vols_container.pop()['ticker'])
            else:
                break

    def process(self, values_to_show=3):
        self.vols_container.sort(key=lambda obj: obj['volatility'], reverse=True)
        self.construct_zero()
        self.max = self.vols_container[:values_to_show]
        self.min = self.vols_container[-values_to_show:]

    def print_values(self):
        print('Максимальная волатильность: ')
        print('+----------+--------------+\n|  TICKER  |      VOL     |\n+----------+--------------+')

        for value in self.max:
            print(f'|{value["ticker"]:^9} - {value["volatility"]:^10.2f} % |')
        print('+----------+--------------+\n')

        print('Минимальная волатильность: ')
        print('+----------+--------------+\n|  TICKER  |      VOL     |\n+----------+--------------+')
        for value in self.min:
            print(f'|{value["ticker"]:^9} - {value["volatility"]:^10.2f} % |')
        print('+----------+--------------+\n')

        print('Нулевая волатильность: ')
        print(', '.join(self.zero))