import matplotlib.pyplot as plt

import simulation


def plotting(data, col1='w_avg_dice', col2='o_avg_dice', choice='strategy'):
    fig, ax = plt.subplots()
    colors = {'blitz': 'blue', 'minimalist': 'red', 'sensible': 'green'}
    for key in colors.keys():
        ax.scatter(x=col1, y=col2, c=colors[key],
                   data=data.loc[data[choice] == key], alpha=min(1/len(data)*15000, 1), marker='.',
                   s=min(1/len(data)*90000, 2), label=key)

    horizontal = min(data[col1]), max(data[col1])
    vertical = min(data[col2]), max(data[col2])

    ax.plot([horizontal[0], horizontal[1]], [0, 0], c='black', alpha=.5)
    ax.plot([0, 0], [vertical[0], vertical[1]], c='black', alpha=.5)

    ax.legend(frameon=False, markerscale=20)

    ls = [x.replace('_', ' ').replace('o', "Other players'").replace('w', 'Winner').replace('avg', 'average')
          for x in [col1, col2]]

    ax.set(xlabel=ls[0], ylabel=ls[1], title=choice.capitalize())

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
    plotting(c[c.tie==True], col2='2nd_avg_dice')
