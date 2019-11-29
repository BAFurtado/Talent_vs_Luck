import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import game_on


def statistics(n):
    output = pd.DataFrame(columns=['tie', 'strategy', 'goal', 'n_countries', 'o_avg_dice',
                                   'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls'])
    for i in range(n):
        print(f'Game {i}')
        # Results of game_on come as a dictionary
        output.loc[i, ] = game_on.main(6, False)
    return output


if __name__ == '__main__':
    m = 10000
    # out = statistics(m)
    # with open(f'results/objects_{m}', 'wb') as f:
    #     pickle.dump(out, f)
    # print(out)
    #
    with open(f'results/objects_{m}', 'rb') as f:
        c = pickle.load(f)
    print(c)
    c[['n_countries', 'o_avg_dice', 'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls']] = c[
        ['n_countries', 'o_avg_dice', 'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls']].astype('float')
    sns.scatterplot(x='o_avg_dice', y='w_avg_dice', hue='strategy', data=c, palette=['red', 'green', 'blue'],
                    alpha=.5, markers='.')
    plt.show()
