from numpy import random

from countries import World
from goals import draw_n_goals, types, possible_enemies, Goal
from players import Player


def gen_world(num_players):
    w = World()
    enemies = random.choice(possible_enemies, num_players, replace=False)
    gls = draw_n_goals(num_players, types, enemies)
    for i in range(num_players):
        p = Player(i)
        p.name = enemies[i]
        while p.goal is None:
            random.shuffle(gls)
            g = gls.pop()
            if g.enemy != p.name:
                p.goal = g
            else:
                p.goal = Goal(random.choice(['territory18', 'territory24']))
        w.players.append(p)
    return w


def main(num_players):
    w = gen_world(num_players)
    return w


if __name__ == '__main__':
    w1 = main(6)
    # Check continents
    a = [lst.goal.to_conquer for lst in w1.players]
    for i in a:
        print(i)
