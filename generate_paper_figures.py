import plot_analysis


def main(n=100000, generate=False):
    c = plot_analysis.simulation.main(n, generate)

    # plotting parameters:
    # data, col1='w_avg_dice', col2='o_avg_dice', choice='strategy'

    # Plotting Figure tie=True
    plot_analysis.plotting(c)

    # Plotting Figure 2nd avg dice
    plot_analysis.plotting(c[c.tie], col2='2nd_avg_dice', tie=True)

    # Plotting Figure tie=False and 2nd ave dice
    # plot_analysis.plotting(c[c.tie == False], col2='2nd_avg_dice')

    p = 'strategy'
    cs = ['sensible', 'minimalist', 'blitz']
    t = 'n_countries'

    # Plotting strategy against num_countries
    plot_analysis.plot_kde(c, cs, p, t)

    t = 'o_avg_dice'
    # Plotting strategy agains other dice
    plot_analysis.plot_kde(c, cs, p, t, True)

    t = 'w_avg_dice'
    # Plotting strategy agains avg_dice
    plot_analysis.plot_kde(c, cs, p, t, True)

    p = 'goal'
    cs = ['territory18', 'territory24', 'continent', 'destroy']
    t = 'n_countries'
    # Plotting goal against num_countries
    plot_analysis.plot_kde(c, cs, p, t, False, 'n_countries_goal')


if __name__ == '__main__':
    # Printing all figures
    main()
