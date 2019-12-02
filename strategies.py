import pickle

import matplotlib.pyplot as plt
import pandas as pd

import game_on


def statistics(n):
    output = pd.DataFrame(columns=['tie', 'strategy', 'goal', 'n_countries', 'o_avg_dice',
                                   'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls'])
    for i in range(n):
        print(f'Game {i}')
        # Results of game_on come as a dictionary
        output.loc[i, ] = game_on.main(6, False)
    return output


def plotting(data, col1='w_avg_dice', col2='o_avg_dice', choice='strategy'):
    fig, ax = plt.subplots()
    colors = {'blitz': 'blue', 'minimalist': 'red', 'random': 'green'}
    for key in colors.keys():
        ax.scatter(x=col1, y=col2, c=colors[key],
                   data=data.loc[c[choice] == key], alpha=.12, marker='.', label=key)

    ax.plot([0, , [0, 0], c='black', alpha=.9)
    ax.legend(frameon=False)

    ls = [x.replace('_', ' ').replace('o', "Other players'").replace('w', 'Winner').replace('avg', 'average')
          for x in [col1, col2]]

    ax.set(xlabel=ls[0], ylabel=ls[1], title=choice.capitalize())

    for each in ['top', 'bottom', 'right', 'left']:
        ax.spines[each].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    plt.tick_params(axis='both', which='both', bottom=True, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)

    plt.savefig('{}_{}.png'.format(col1, col2), bbox_inches='tight')
    plt.show()


def summary(data):
    data.groupby(by=['strategy', 'goal', 'tie']).agg(['mean', 'count']).to_csv('summary.csv', sep=';')


if __name__ == '__main__':
    m = 10000
    generate = False
    if generate:
        c = statistics(m)
        with open(f'results/objects_{m}', 'wb') as f:
            pickle.dump(c, f)
        print(c)
    else:
        with open(f'results/objects_{m}', 'rb') as f:
            c = pickle.load(f)
        print(c)
    c[['n_countries', 'o_avg_dice', 'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls']] = \
        c[['n_countries', 'o_avg_dice', 'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls']].astype('float')
    plotting(c)
    summary(c)

