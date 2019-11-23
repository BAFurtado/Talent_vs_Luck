import pickle
import game_on
from collections import Counter


def statistics(n):
    output = list()
    for i in range(n):
        print(f'Game {i}')
        output.append(game_on.main(6, False))
    return output


if __name__ == '__main__':
    m = 100000
    out = statistics(m)
    c = Counter(out)
    with open('objects', 'wb') as f:
        pickle.dump(c, f)
    print(c)
