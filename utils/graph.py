import networkx as nx
import matplotlib.pyplot as plt


from countries import load_data, data


def generate_map(l):
    G = nx.Graph()
    G.add_nodes_from([c.id for c in l])
    G.add_edges_from(data['connections'])
    return G


if __name__ == '__main__':
    cts = load_data()
    g = generate_map(cts)
    plt.subplot()
    nx.draw_networkx(g, )
    plt.show()
