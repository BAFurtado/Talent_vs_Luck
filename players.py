from collections import Counter

import networkx as nx


class Player:
    def __init__(self, _id):
        self.id = _id
        self.name = None
        self.strategy = None
        self.goal = None
        self.my_countries = list()

    def add_country(self, world, country, army=1):
        self.my_countries.append(country)
        country.owner = self
        country.army = army
        nx.set_node_attributes(world.net, {country.id: {'owner': self.name}})

    def remove_country(self, world, country):
        self.my_countries.remove(country)
        country.owner = None
        country.army = 0
        nx.set_node_attributes(world.net, {country.id: {'owner': None}})

    def num_countries(self):
        return len(self.my_countries)

    def full_continent(self, world):
        armies = dict()
        stats = self.prop_continent(world)
        if 1 in stats.values():
            for k, v in stats.items():
                if v == 1:
                    armies[k] = stats[k]
        return armies

    def prop_continent(self, world):
        prop = Counter([i.continent for i in self.my_countries])
        return {k: prop[k] / len(world.data['continents'][k]) for k in prop.keys()}

    def ordered_continent(self, world):
        stats = self.prop_continent(world)
        return sorted(stats.items(), key=lambda key: stats[key])

    def calculate_army(self, world):
        armies = self.full_continent(world)
        armies['general'] = self.num_countries() // 2
        return armies

    def define_priorities(self, world):
        neighbors = set([key for c in self.my_countries for key in world.net[c.id].keys()])
        if self.strategy == 'random':
            return neighbors

    def allocate_armies(self):
        pass


if __name__ == '__main__':
    p1 = Player(0)
