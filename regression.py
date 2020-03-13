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


def prepare_data(data, machine=False):
    y = data.success.astype(int)
    dummies = pd.get_dummies(data, columns=['strategy', 'goal', 'context'])
    # Getting baselines:
    # For Strategy: Base is Minimalist.
    # For Goal: Base is Territory18.
    # Getting ALL of the contexts using iloc
    include = ['strategy_blitz', 'strategy_sensible', 'goal_continent', 'goal_territory24', 'goal_destroy']
    # Using last game as baseline
    context = [col for col in dummies if col.startswith('context')]
    if machine:
        include += ['strategy_minimalist', 'goal_territory18']
        context = context[:-1]
    x = pd.concat([data.luck.astype(float), dummies[include].astype(int), dummies[context].astype(int)], axis=1)
    return x.to_numpy(), y.to_numpy(), ['luck'] + include + context


def regress(x, y, cols):
    lm = sm.Logit(y, x)
    # pm = sm.Probit(y, x)
    res_lm = lm.fit()
    # res_pm = pm.fit()
    print(res_lm.summary2(yname='Success', xname=cols, title='Logit Regression'))
    # print(res_pm.summary2(yname='Success', xname=cols, title='Logit Regression'))

    # Plotting
    # for i in range(len(cols)):
    #     plt.scatter(x[i], y, label=cols[i])
    #     plt.show()
    return res_lm


if __name__ == "__main__":
    gen = False
    d = get_data(10000, gen)
    X, Y, C = prepare_data(d)
    res = regress(X, Y, C)
    # Further processing results
    head_details = pd.read_html(res.summary(yname='Success', xname=C).tables[0].as_html(), header=0, index_col=0)[0]
    results_body = pd.read_html(res.summary(yname='Success', xname=C).tables[1].as_html(), header=0, index_col=0)[0]
    head2 = pd.read_html(res.summary2(yname='Success', xname=C).as_html())[0]
    # with open(f'results/results_reg_bundle', 'wb') as f:
    #     pickle.dump([head_details, results_body, head2], f)
