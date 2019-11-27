# Country data from
# https://github.com/AlexWilton/Risk-World-Domination-Game/blob/master/data/default_map.json

# 6 continents
# 83 connections among countries (all pairs as lists)

import json

import networkx as nx

with open('utils/map.json', 'r') as f:
    data = json.load(f)


def load_data():
    countries = dict()
    for each in data['country_names'].items():
        c = Country(int(each[0]), each[1])
        for key in data['continents'].keys():
            if int(each[0]) in data['continents'][key]:
                c.continent = key
                break
        for conn in data['connections']:
            if c.id in conn:
                c.neighbors.append(conn)
        c.neighbors = [j for i in c.neighbors for j in i if j != c.id]
        countries[c.id] = c
    return countries


class Country:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.continent = list()
        self.neighbors = list()
        self.owner = None
        self.army = 0

    def __str__(self):
        return f'Country {self.name} -- id no. {self.id}. Army: {self.army} is in continent {self.continent}\n' \
               f'My neighbors are {self.neighbors}\n'


class World:
    def __init__(self):
        self.countries = load_data()
        self.data = data
        self.players = list()
        self.turn = 0
        self.net = self.generate_map()
        self.on = True
        self.winner = None
        self.log = None

    def generate_map(self):
        G = nx.Graph()
        G.add_nodes_from(self.countries.keys())
        G.add_edges_from(self.data['connections'])
        return G

    def distribute_countries(self):
        if self.turn == 0:
            i = 0
            while i < len(self.countries):
                for p in self.players:
                    p.add_country(self, self.countries[i])
                    i += 1

    def deploy_army(self):
        for p in self.players:
            p.allocate_armies(self)

    def play_turn(self):
        # Animation won't work with while. It has to be an IF
        if self.on:
            if self.log:
                self.log.info(f'Playing turn {self.turn}')
            for p in self.players:
                # Check if last player did not win with 'destroy' goal
                if self.on:
                    p.attack(self)
                    # Again checking goals before rearranging
                    if self.on:
                        p.rearrange(self)
                        # Check Winner!
                        p.goal.update_goal(self.countries)
                        if p.goal.check_goal(p):
                            if self.log:
                                arms = sum([c.army for c in p.my_countries.values()])
                                self.log.info(f"{p.name.capitalize()} is the WINNER, with {arms} armies, "
                                              f"goal: '{p.goal.type}' and enemy {p.goal.enemy} "
                                              f"with strategy {p.strategy}")
                            self.winner = p
                            self.on = False
            self.turn += 1
            if self.turn > 200:
                self.on = False
                self.winner = 'Tie'


if __name__ == '__main__':
    cts = load_data()
    print(cts[0], cts[-1])
