from countries import World
from players import Player
from goals import draw_n_goals, types, possible_enemies
from numpy import random


def gen_world(num_players):
    w = World()
    enemies = random.choice(possible_enemies, num_players, replace=False)
    gls = draw_n_goals(num_players, types, enemies)
    for i in range(num_players):
        p = Player(i)
        p.name = enemies[i]
        while p.goal is None:
            random.shuffle(gls)
            g = random.choice(gls, replace=False)
            if g.enemy != p.name:
                p.goal = g
            else:
                gls.append(g)
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
