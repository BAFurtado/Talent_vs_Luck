from collections import Counter

import networkx as nx


class Player:
    def __init__(self, _id):
        self.id = _id
        self.name = None
        self.strategy = None
        self.goal = None
        self.my_countries = dict()

    def add_country(self, world, country, army=1):
        self.my_countries[country.id] = country
        country.owner = self
        country.army = army
        nx.set_node_attributes(world.net, {country.id: {'owner': self.name}})

    def remove_country(self, world, country):
        self.my_countries.pop(country, None)
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
        prop = Counter([i.continent for i in self.my_countries.values()])
        return {k: prop[k] / len(world.data['continents'][k]) for k in prop.keys()}

    def ordered_continent(self, world):
        stats = self.prop_continent(world)
        return sorted(stats, key=(lambda k: stats[k]), reverse=True)

    def calculate_army(self, world):
        armies = self.full_continent(world)
        armies['general'] = self.num_countries() // 2
        return armies

    def define_priorities(self, world):
        c_ids = self.my_countries.keys()
        neighbors = [n for c in self.my_countries.values() for n in c.neighbors if n not in c_ids]

        # Independent of strategy, seek continent completion first
        priority = list()
        for i in self.ordered_continent(world):
            for j in world.data['continents'][i]:
                if (j in neighbors) and (j not in c_ids):
                    priority.append(j)
        # Completing the rest of the list
        for each in neighbors:
            if each not in priority:
                priority.append(each)

        # Which country to attack with which priority
        tup_results = [(c.id, p) for p in priority for c in self.my_countries.values() if p in c.neighbors]
        # Eliminating double targets
        targets = list()
        attack_priority = list()
        for each in tup_results:
            if each[1] not in targets:
                targets.append(each[1])
                attack_priority.append(each)
        return attack_priority

    def allocate_armies(self, world):
        armies = self.calculate_army(world)
        attack_priority = self.define_priorities(world)
        for a in attack_priority:
            max_territory = 3
            while armies['general'] > 0 and max_territory > 0:
                self.my_countries[a[0]].army += 1
                max_territory -= 1
                armies['general'] -= 1


if __name__ == '__main__':
    p1 = Player(0)
