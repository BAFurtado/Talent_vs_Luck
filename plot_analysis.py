import matplotlib.pyplot as plt
import seaborn as sns
import simulation


def plot_kde(data, cols, per, target, vline=False, lab=None):
    fig, ax = plt.subplots()
    for col in cols:
        ax = sns.kdeplot(data[data[per] == col][target], shade=True, label=col)
    sns.despine()
    ax.legend(frameon=False, fontsize='x-large')
    if vline:
        ax.axvline(x=0, color='gray', linewidth=3, alpha=.5)
    if not lab:
        lab = target
    # ax.set_title(lab)
    plt.show()
    fig.savefig(f"results/{lab.replace(' ', '_')}.png")
    fig.savefig(f"results/{lab.replace(' ', '_')}.pdf")


def plotting(data, col1='w_avg_dice', col2='o_avg_dice', choice='strategy'):
    fig, ax = plt.subplots()
    colors = {'blitz': 'blue', 'minimalist': 'red', 'sensible': 'green'}
    for key in colors.keys():
        ax.scatter(x=col1, y=col2, c=colors[key],
                   data=data.loc[data[choice] == key], marker='.',
                   s=min(1/len(data)*90000, 2), label=key, )
    horizontal = min(data[col1]), max(data[col1])
    vertical = min(data[col2]), max(data[col2])

    ax.plot([horizontal[0], horizontal[1]], [0, 0], c='black', lw=2, alpha=.5)
    ax.plot([0, 0], [vertical[0], vertical[1]], c='black', lw=2, alpha=.5)

    ax.legend(frameon=False, markerscale=5, fontsize='x-large')

    ls = [x.replace('_', ' ').replace('o', "Other players'").replace('w', 'Winner').replace('avg', 'average')
          for x in [col1, col2]]

    ax.set(xlabel=ls[0], ylabel=ls[1])

    for each in ['top', 'bottom', 'right', 'left']:
        ax.spines[each].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)
    plt.tick_params(axis='both', which='both', bottom=True, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)

    plt.savefig('results/{}_{}.png'.format(col1, col2), bbox_inches='tight')
    plt.savefig('results/{}_{}.pdf'.format(col1, col2), bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    m = 100000
    gen = False
    c = simulation.main(m, gen)
    # plotting(c)
    # plotting(c[c.tie], col2='2nd_avg_dice')
    # plotting(c[c.tie == False], col2='2nd_avg_dice')
    # p = 'strategy'
    # cs = ['sensible', 'minimalist', 'blitz']
    # t = 'n_countries'
    # plot_kde(c, cs, p, t)
    # t = 'o_avg_dice'
    # plot_kde(c, cs, p, t)
    # t = 'w_avg_dice'
    # plot_kde(c, cs, p, t)
    # p = 'goal'
    # cs = ['territory18', 'territory24', 'continent', 'destroy']
    # t = 'n_countries'
    # plot_kde(c, cs, p, t, 'n_countries_goal')
