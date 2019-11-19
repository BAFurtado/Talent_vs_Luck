import matplotlib.pyplot as plt
import networkx as nx
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
    w.distribute_countries()
    return w


if __name__ == '__main__':
    w1 = main(6)
    nx.draw(w1.net, with_labels=True, node_color=[w1.net.nodes[i]['owner'] for i in w1.net.nodes])
    plt.show()

