import pickle
from collections import Counter

import game_on


def statistics(n):
    output = list()
    for i in range(n):
        print(f'Game {i}')
        output.append(game_on.main(6, False))
    return output


if __name__ == '__main__':
    m = 100
    out = statistics(m)
    c = Counter(out)
    with open(f'objects_{m}', 'wb') as f:
        pickle.dump(c, f)
    print(c)
