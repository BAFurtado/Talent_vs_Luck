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

    # Table4 -- Luck
    print('______________________________________________________')
    print('Table IV -- Luck')
    print(c[['w_avg_dice', '2nd_avg_dice', 'o_avg_dice']].median())
    print(c.groupby(by='tie').agg('median')[['w_avg_dice', '2nd_avg_dice', 'o_avg_dice']])
    print(c.groupby(by='strategy').agg('median')[['w_avg_dice', '2nd_avg_dice', 'o_avg_dice']])

    # Table5 -- Luck by strategy and tie
    print('______________________________________________________')
    print('Table V')
    print(c.groupby(by=['tie', 'strategy']).agg('median')[['w_avg_dice', '2nd_avg_dice', 'o_avg_dice']])

    # Table6 Resilience and Opportunity
    print('______________________________________________________')
    print('Table VI')
    print(c.groupby(by=['strategy', 'tie']).agg(['count', 'median'])[['w_num_rolls', 'o_avg_num_rolls',
                                                                      'w_avg_dice', 'o_avg_dice']])
    return c


if __name__ == '__main__':
    df = main()
