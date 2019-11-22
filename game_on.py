import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import animation
from numpy import random

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


def update(num, world, ax):
    ax.clear()
    # Set the title
    ax.set_title(f'Turn {world.turn}')
    nx.draw_networkx(world.net, with_labels=True, pos=nx.kamada_kawai_layout(world.net),
                     node_color=[world.net.nodes[i]['owner'] for i in world.net.nodes], tight_layout=False)
    world.play_turn()


def animating(world):
    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(fig, update, fargs=(world, ax), interval=600)
    ani.save('game.gif', writer='imagemagick')
    # plt.show()


def main(num_players, animate=True):
    w = gen_world(num_players)
    w.distribute_countries()
    w.deploy_army()
    # number of frames in animation determines number of runs of 'world.play_run'
    if animate:
        animating(w)
    else:
        while w.on:
            w.play_turn()
    return w


if __name__ == '__main__':
    w1 = main(6, False)
    p1 = w1.players[0]
