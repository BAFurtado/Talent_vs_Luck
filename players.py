from collections import Counter

import networkx as nx
from numpy import random

import battle


class Player:
    def __init__(self, _id):
        self.id = _id
        self.name = None
        self.strategy = None
        self.goal = None
        self.my_countries = dict()
        self.playing = True

    def add_country(self, world, country, army=1):
        self.my_countries[country.id] = country
        country.owner = self
        country.army = army
        nx.set_node_attributes(world.net, {country.id: {'owner': self.name}})

    def remove_country(self, world, country):
        country.owner = None
        country.army = 0
        nx.set_node_attributes(world.net, {country.id: {'owner': None}})
        del self.my_countries[country.id]

    def num_countries(self):
        return len(self.my_countries)

    def full_continent(self, world):
        armies = dict()
        stats = self.prop_continent(world)
        if 1 in stats.values():
            for k, v in stats.items():
                if v == 1:
                    armies[k] = world.data['continent_values'][k]
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
        # Assign minimum of three armies per player
        if armies['general'] < 3:
            armies['general'] = 3
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
            if self.strategy == 'blitz':
                max_territory = armies['general']
            else:
                max_territory = 3
            while armies['general'] > 0 and max_territory > 0:
                self.my_countries[a[0]].army += 1
                max_territory -= 1
                armies['general'] -= 1

            # Allocate continent army
            if len(armies.keys()) > 1:
                for key in armies.keys():
                    if len(key) == 1 and armies[key] > 0:
                        if self.my_countries[a[0]] in world.data['continents'][key]:
                            self.my_countries[a[0]].army = armies[key]
                            armies[key] = 0
                            break
                        else:
                            for i in range(armies[key]):
                                # Pick a random country within the continent
                                c = random.choice(world.data['continents'][key])
                                self.my_countries[c].army += 1
                            armies[key] = 0

    def attack(self, world):
        if world.turn != 0:
            self.allocate_armies(world)
        attack_priority = self.define_priorities(world)
        for a in attack_priority:
            attacker = self.my_countries[a[0]]
            if attacker.army > 1:
                defender = world.countries[a[1]]
                # Attack until winning or exhausting army
                a, d = battle.battle(attacker.army, defender.army)
                if d == 0:
                    temp_defender = defender.owner
                    defender.owner.remove_country(world, defender)
                    # Check number of armies to pass
                    if a > 4:
                        self.add_country(world, defender, a - 3)
                        attacker.army -= a - 3
                    else:
                        self.add_country(world, defender, a - 1)
                        attacker.army -= a - 1

                    # Check if loser is done
                    if len(temp_defender.my_countries) == 0:
                        temp_defender.playing = False
                        # print(f'{temp_player.name} is out of the game')
                        if attacker.owner.goal.enemy == temp_defender.name:
                            world.winner = (attacker.owner.strategy, attacker.owner.goal.type)
                            world.on = False
                    if self.strategy == 'minimalist':
                        return
                else:
                    attacker.army = a
                    defender.army = d

    def rearrange(self, world):
        if self.strategy == 'random':
            pass
        else:
            if self.strategy == 'blitz':
                # protect hubs
                min_army = 1
            else:
                # minimalist, protection across countries
                min_army = 2
            # collect extra armies
            extra = 0
            for key in self.my_countries.keys():
                if self.my_countries[key].army > min_army:
                    self.my_countries[key].army -= self.my_countries[key].army - min_army
                    extra += self.my_countries[key].army - min_army
            priorities = self.define_priorities(world)
            i = 0
            while extra > 0:
                self.my_countries[priorities[i][0]].army += 1
                extra -= 1
                i += 1
                i = i % len(self.my_countries.keys())


if __name__ == '__main__':
    p1 = Player(0)
