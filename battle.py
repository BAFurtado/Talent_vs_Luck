from numpy import random


def roll(n=1):
    return random.choice(range(1, 7), n)


def combat(attack=1, defense=1):
    # Single attack. Number of soldiers on attack, defense
    p1 = sorted(roll(attack), reverse=True)
    p2 = sorted(roll(defense), reverse=True)
    a, d = 0, 0
    for i in range(min(attack, defense)):
        if p1[i] > p2[i]:
            a += 1
        else:
            d += 1
    # Return number of losses on either side
    return a, d


def battle(n_att, n_def):
    # Attack until win or exhaust Army
    while n_att > 1:
        a, d = combat(min(n_att - 1, 3), min(n_def, 3))
        n_att -= d
        n_def -= a
        if n_def == 0:
            return n_att, n_def
    return n_att, n_def


if __name__ == '__main__':
    print(battle(1, 1))
    # m = 5000
    # res = 0
    # for i in range(m):
    #     att, _def = battle(4, 3)
    #     if att > _def:
    #         res += 1
    # print(res/m)
