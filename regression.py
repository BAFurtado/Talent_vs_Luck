
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
import pickle

import game_on


def get_data(n, generate=True):
    if generate:
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
    x = pd.concat([dummies[['strategy_blitz', 'strategy_sensible', 'goal_continent', 'goal_territory24',
                            'goal_destroy']], data.tie, data.opportunity, data.luck, dummies.iloc[:, 10:]], axis=1)
    return x.to_numpy(), y.to_numpy(), x.columns


def regress(x, y, cols):
    lm = LogisticRegression(solver='lbfgs')
    lm.fit(x, y)

    # Inputs are y and fitted model predict(x)
    for i in range(8):
        print('{} coefficient is {:.4}'.format(cols[i], lm.coef_[0][i]))

    print('R2 score {:.4}'.format(r2_score(y, lm.predict(x))))

    # Plotting
    # for i in range(len(cols)):
    #     plt.scatter(x[i], y, label=cols[i])
    #     plt.show()
    # print(lm)

    return lm


if __name__ == "__main__":
    gen = True
    d = get_data(1000)
    X, Y, C = prepare_data(d)
    reg = regress(X, Y, C)
