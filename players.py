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

    def calculate_army(self, world):
        armies = self.full_continent(world)
        armies['general'] = self.num_countries() // 2
        return armies

    def full_continent(self, world):
        armies = dict()
        cts = [str(x.id) for x in self.my_countries]
        for k, v in world.data['continents'].items():
            if set(v).issubset(cts):
                armies[k] = world.data['continent_values'][k]
        return armies

    def define_priorities(self, world):
        pass

    def allocate_armies(self):
        pass


if __name__ == '__main__':
    p1 = Player(0)
