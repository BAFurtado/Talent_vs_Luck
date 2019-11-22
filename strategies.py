import game_on
from collections import Counter


def statistics(n):
    output = list()
    for i in range(n):
        print(f'Game {i}')
        output.append(game_on.main(6, False))
    return output


if __name__ == '__main__':
    # TODO: Check 'destroy' by the player itself, otherwise territory24
    m = 100
    out = statistics(m)
    print(Counter(out))
