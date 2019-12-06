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
    colors = {'blitz': 'blue', 'minimalist': 'red', 'sensible': 'green'}
    for key in colors.keys():
        ax.scatter(x=col1, y=col2, c=colors[key],
                   data=data.loc[c[choice] == key], alpha=.15, marker='.', s=.9, label=key)

    horizontal = min(data[col1]), max(data[col1])
    vertical = min(data[col2]), max(data[col2])

    ax.plot([horizontal[0], horizontal[1]], [0, 0], c='black', alpha=.5)
    ax.plot([0, 0], [vertical[0], vertical[1]], c='black', alpha=.5)

    ax.legend(frameon=False, markerscale=20)

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
    data = data.groupby(by=['strategy', 'goal', 'tie']).agg(['mean', 'count'])
    data = data.reset_index()
    data.columns = data.columns.droplevel(1)
    d1 = data.iloc[:, :5]
    d2 = data.iloc[:, [5, 7, 9, 11]]
    data = pd.concat([d1, d2], axis=1)
    data.columns = ['strategy', 'goal', 'tie', 'n_countries', 'num_wins', 'o_avg_dice',
                 'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls']
    data.to_csv('summary.csv', sep=';', index=False)
    return data


def main(n=10000, generate=True):
    if generate:
        c = statistics(n)
        with open(f'results/objects_{n}', 'wb') as f:
            pickle.dump(c, f)
        print(c)
    else:
        with open(f'results/objects_{n}', 'rb') as f:
            c = pickle.load(f)
        print(c)
    c[['n_countries', 'o_avg_dice', 'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls']] = \
        c[['n_countries', 'o_avg_dice', 'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls']].astype('float')
    plotting(c)
    s = summary(c)
    return s


if __name__ == '__main__':
    m = 10000
    gen = False
    main(m, gen)