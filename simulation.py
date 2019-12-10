import pickle

import pandas as pd

import game_on


def statistics(n):
    output = pd.DataFrame(columns=['tie', 'strategy', 'goal', 'n_countries', 'o_avg_dice',
                                   'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls',
                                   '2nd_avg_dice', '2nd_num_rolls'])
    for i in range(n):
        print(f'Game {i}')
        # Results of game_on come as a dictionary
        output.loc[i, ] = game_on.main(6, False)
    return output


def summary(data):
    data = data.groupby(by=['strategy', 'goal', 'tie']).agg(['mean', 'count'])
    data = data.reset_index()
    data.columns = data.columns.droplevel(1)
    d1 = data.iloc[:, :5]
    d2 = data.iloc[:, [5, 7, 9, 11, 13, 15]]
    data = pd.concat([d1, d2], axis=1)
    data.columns = ['strategy', 'goal', 'tie', 'n_countries', 'num_wins', 'o_avg_dice', 'w_avg_dice', 'w_num_rolls',
                    'o_avg_num_rolls', '2nd_avg_dice', '2nd_num_rolls']
    data.to_csv('summary.csv', sep=';', index=False)
    return data


def main(n=10000, generate=True):
    if generate:
        c = statistics(n)
        with open(f'results/objects_{n}', 'wb') as f:
            pickle.dump(c, f)
    else:
        with open(f'results/objects_{n}', 'rb') as f:
            c = pickle.load(f)
    c[['n_countries', 'o_avg_dice', 'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls', '2nd_avg_dice', '2nd_num_rolls']] = \
        c[['n_countries', 'o_avg_dice', 'w_avg_dice', 'w_num_rolls', 'o_avg_num_rolls', '2nd_avg_dice',
           '2nd_num_rolls']].astype('float')
    s = summary(c)
    print(s)
    return c


if __name__ == '__main__':
    m = 100000
    gen = True
    o = main(m, gen)
