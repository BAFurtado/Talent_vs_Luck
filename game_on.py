import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import animation
from numpy import random
import logging
from numpy import cumsum

from countries import World
from goals import draw_n_goals, types, possible_enemies, Goal, strategies
from players import Player


def gen_world(num_players):
    w = World()
    enemies = random.choice(possible_enemies, num_players, replace=False)
    gls = draw_n_goals(num_players, types, enemies)
    for i in range(num_players):
        p = Player(i)
        p.name = enemies[i]
        p.strategy = random.choice(strategies)

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
    labels = {k: world.countries[k].army for k in world.countries.keys()}
    nx.draw_networkx(world.net, pos=nx.kamada_kawai_layout(world.net), labels=labels,
                     node_color=[world.net.nodes[i]['owner'] for i in world.net.nodes], tight_layout=False, )
    world.play_turn()


def animating(world):
    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(fig, update, frames=200, fargs=(world, ax), interval=800, repeat_delay=0)
    ani.save('game.gif', writer='pillow')
    plt.show()


def main(num_players, animate):
    w = gen_world(num_players)
    if animate:
        w.log = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)
    w.distribute_countries()
    w.deploy_army()
    # number of frames in animation determines number of runs of 'world.play_run'
    if animate:
        animating(w)
    else:
        while w.on:
            w.play_turn()
    # return w.winner
    return w


if __name__ == '__main__':
    anim = True
    # winner = main(6, anim)
    w = main(6, anim)
    for p in w.players:
        print(f'{sum(p.dice)/len(p.dice):.4f}, {len(p.dice)}, '
              f'{len(p.my_countries)}, {p.name}, {p.strategy}, {p.goal.type}')
        plt.plot(cumsum(p.dice), color=p.name)
    plt.show()
    # if anim:
    #     import os
    #     if os.path.exists('game.gif'):
    #         os.remove('game.gif')
    #     os.system("ffmpeg -i game.mp4 game.gif")
