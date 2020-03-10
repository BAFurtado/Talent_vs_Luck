
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

import game_on
import simulation


def prepare_data(n):
    data = pd.DataFrame(columns=['success', 'strategy', 'luck', 'goal', 'context', 'tie', 'opportunity'])
    for i in range(n):
        print(f'Game {i}')
        # Results of game_on for regression come as a DataFrame
        game_data, world = game_on.main(6, False, process_dataframe=False, process_reg=True)
        game_data['context'] = i
        data = pd.concat([data, game_data], ignore_index=True)
    return data


def regress(X, y):
    lm = LinearRegression()
    lm.fit(X, y)

    # Inputs are Y and fitted model predict(X)
    for each in range(len(X.columns)):
        print('{} coefficient is {:.4}'.format(X.columns[each], lm.coef_[each]))

    print('R2 score {:.4}'.format(r2_score(data.sales, lm.predict(X))))

    # Plotting
    plt.scatter(X.TV, y, color='r')
    plt.scatter(X.radio, y, color='b')
    plt.scatter(X.newspaper, y, color='g')
    plt.show()
    print(lm)


if __name__ == "__main__":
    d = prepare_data(5)
