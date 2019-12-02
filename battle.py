from numpy import random


def roll(n=1):
    return random.choice(range(1, 7), n)


def combat(attacker, defender, attack=1, defense=1):
    # Single attack. Number of soldiers on attack, defense
    p1 = sorted(roll(attack), reverse=True)
    p2 = sorted(roll(defense), reverse=True)
    a, d = 0, 0
    for i in range(min(attack, defense)):
        # If player wins, he adds 1 to his list of rolls. Else, adds -1
        # That is the win or loss of each of the dice the player rolls
        if p1[i] > p2[i]:
            a += 1
            attacker.owner.dice.append(1)
            defender.owner.dice.append(-1)
        else:
            d += 1
            attacker.owner.dice.append(-1)
            defender.owner.dice.append(1)
    # Return number of paired wins on either side
    return a, d


def battle(attacker, defender):
    n_att = attacker.army
    n_def = defender.army
    # Attack until win or exhaust Army
    while n_att > 1:
        a, d = combat(attacker, defender, min(n_att - 1, 3), min(n_def, 3))
        n_att -= d
        n_def -= a
        if n_def == 0:
            return n_att, n_def
    # Return number of armies left on either side
    return n_att, n_def


if __name__ == '__main__':
    pass
    # m = 5000
    # res = 0
    # for i in range(m):
    #     att, _def = battle(4, 3)
    #     if att > _def:
    #         res += 1
    # print(res/m)
