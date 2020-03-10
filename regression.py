
import simulation
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np


def prepare_data(data):
    pass


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
    data = simulation.main(100, True)
