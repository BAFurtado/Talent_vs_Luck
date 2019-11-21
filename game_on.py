import matplotlib.pyplot as plt
import networkx as nx
from numpy import random

from matplotlib import animation

import strategies
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
        p.strategy = random.choice(strategies.strategies)
        random.shuffle(gls)
        g = gls.pop()
        if g.enemy != p.name:
            p.goal = g
        else:
            p.goal = Goal(random.choice(['territory18', 'territory24']))
        w.players.append(p)
    return w


def update(num, G, world, ax):
    ax.clear()
    world.play_turn()
    nx.draw_networkx(G, with_labels=True, pos=nx.kamada_kawai_layout(G),
                     node_color=[G.nodes[i]['owner'] for i in G.nodes], tight_layout=False)


def animating(world):
    fig, ax = plt.subplots()
    G = world.net
    ani = animation.FuncAnimation(fig, update, frames=20, fargs=(G, world, ax))
    ani.save('game.gif', writer='imagemagick')
    plt.show()


def main(num_players):
    w = gen_world(num_players)
    w.distribute_countries()
    w.deploy_army()
    animating(w)
    return w


if __name__ == '__main__':
    w1 = main(6)
    p1 = w1.players[0]
