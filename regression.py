import os
import pickle

import pandas as pd
import statsmodels.api as sm

import game_on


def get_data(n, generate=True):
    if generate or not os.path.exists(f'results/reg_{n}'):
        data = pd.DataFrame(columns=['success', 'strategy', 'luck', 'goal', 'context', 'tie', 'opportunity'])
        for i in range(n):
            print(f'Game {i}')
            # Results of game_on for regression come as a DataFrame
            game_data, world = game_on.main(6, False, process_dataframe=False, process_reg=True)
            game_data['context'] = i
            data = pd.concat([data, game_data], ignore_index=True)
            with open(f'results/reg_{n}', 'wb') as f:
                pickle.dump(data, f)
    else:
        with open(f'results/reg_{n}', 'rb') as f:
            data = pickle.load(f)
    return data


def prepare_data(data):
    y = data.success.astype('int')
    dummies = pd.get_dummies(data, columns=['strategy', 'goal', 'context'])
    # Getting baselines:
    # For Strategy: Base is Minimalist.
    # For Goal: Base is Territory18.
    # Getting ALL of the contexts using iloc
    include = ['strategy_blitz', 'strategy_sensible', 'goal_continent', 'goal_territory24', 'goal_destroy']
    context = [col for col in dummies if col.startswith('context')]
    x = pd.concat([data.luck, dummies[include], dummies[context]], axis=1)
    return x, y


def regress(x, y):
    lm = sm.Logit(y, x)
    result = lm.fit()
    print(result.summary2())

    # Plotting
    # for i in range(len(cols)):
    #     plt.scatter(x[i], y, label=cols[i])
    #     plt.show()
    return lm


if __name__ == "__main__":
    gen = False
    d = get_data(10000, gen)
    X, Y = prepare_data(d)
    reg = regress(X, Y)
