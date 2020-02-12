import pandas as pd

import simulation


def main(n=100000, generate=False):
    # Read saved data
    c = simulation.main(n, generate)

    # Table1
    print('Table I -- Number of wins by strategy')
    c2 = c.groupby('strategy').agg('count').iloc[:, 0]
    print(c2)

    # Table2
    print('______________________________________________________')
    print('Table II -- Number of wins by ties and strategy')
    c3 = c.groupby(['tie', 'strategy']).agg('count').iloc[:, 0]
    print(c3)
    print(c3.groupby(level=[0]).sum())

    # Table3
    print('______________________________________________________')
    print('Table III -- Number of wins by goals')
    c4 = c.groupby('goal').agg('count').iloc[:, 0]
    print(c4)
    return c


if __name__ == '__main__':
    df = main()
