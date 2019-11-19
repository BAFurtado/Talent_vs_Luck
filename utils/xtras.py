from itertools import groupby

import matplotlib.pyplot as plt

from battle import roll


def probs(n):
    draws = roll(n)
    draws_dict = {value: len(list(freq)) for value, freq in groupby(sorted(draws))}
    return {key: value/n for key, value in draws_dict.items()}


def plotting(n):
    fig, ax = plt.subplots()
    x, y = list(), list()
    for i in range(100, n):
        x.append(i)
        y.append(probs(i)[1])
    ax.plot(x, y, '.', markersize=2)
    ax.plot(x, [1/6] * len(x), lw=2)
    plt.show()


if __name__ == '__main__':
    m = 2000
    out = probs(m)
    for k in out.keys():
        print(k, f'{out[k]:.4f}')
    plotting(m)
