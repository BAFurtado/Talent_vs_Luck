# Country data from
# https://github.com/AlexWilton/Risk-World-Domination-Game/blob/master/data/default_map.json

# 6 continents
# 83 connections among countries (all pairs as lists)

import json

with open('map.json', 'r') as f:
    data = json.load(f)


class Country:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.continent = list()
        self.neighbors = list()

    def __str__(self):
        return f'Country {self.name} -- id no. {self.id} is in continent {self.continent}\n' \
               f'My neighbors are {self.neighbors}\n'


def load_data():
    countries = list()
    for each in data['country_names'].items():
        c = Country(int(each[0]), each[1])
        for key in data['continents'].keys():
            if each[0] in data['continents'][key]:
                c.continent = key
                break
        for conn in data['connections']:
            if c.id in conn:
                c.neighbors.append(conn)
        c.neighbors = [j for i in c.neighbors for j in i if j != c.id]
        countries.append(c)
    return countries


if __name__ == '__main__':
    cts = load_data()
    print(cts[0], cts[-1])
