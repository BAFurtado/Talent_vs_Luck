"""   https://boardgamegeek.com/thread/60929/mission-cards

i) Kill a certain colour. There are 6 of these, one for each colour. If fewer than 6 colours are going to be used in
the game then the cards corresponding to the unused colours are removed from the deck before missions are given out.
(This is quite clearly stated in at least some versions of the rules, and failing to do so doesn't make much sense.)
If you draw your own colour, then your mission changes to mission (iv).

ii) Conquer some combination of continents. There are 6 of these:

Conquer Asia and South America;
Conquer Asia and Africa;
Conquer North America and Africa;
Conquer North America and Australasia;
Conquer Europe and South America and a 3rd continent of your choice [this mission is omitted from 1998 US edition];
Conquer Europe and Australasia and a 3rd continent of your choice [this mission is omitted from 1998 US edition].

iii) Occupy 18 territories with at least 2 armies in each territory.

iv) Occupy 24 territories (no restriction to 2 or more armies in each). """

"""
Blitz. Allocate all to first priority

Minimalist. Conquer one territory, stop.

Sensible. Maximum of 3 on deploying, no rearranging
"""

from numpy import random

from countries import data

strategies = ['sensible', 'minimalist', 'blitz']
continent_goals = [['Asia', 'South America'], ['Asia', 'Africa'], ['North America', 'Africa'],
                   ['North America', 'Asia', 'Australia']]
continent_goals_keys = [['4', '1'], ['4', '3'], ['0', '3'], ['0', '4', '5']]
types = ['continent', 'destroy', 'territory18', 'territory24']
possible_enemies = ['aqua', 'silver', 'plum', 'salmon', 'gold', 'forestgreen']


def generate_continent_goals():
    ctn_goals = list()
    for each in continent_goals_keys:
        to_conquer = list()
        for e in each:
            to_conquer += data['continents'][e]
        ctn_goals.append(to_conquer)
    return ctn_goals


class Goal:
    def __init__(self, _type=None, enemy=None):
        self.type = _type
        self.enemy = enemy
        self.to_conquer = list()

    def update_goal(self, countries):
        if self.type == 'destroy':
            self.to_conquer = [c for c in countries.values() if c.owner.name == self.enemy]

    def check_goal(self, world, player):
        if player.playing:
            if self.type == 'territory18':
                if len([c for c in player.my_countries.values() if c.army > 1]) > 17:
                    return True
                return False
            elif self.type == 'territory24':
                if player.num_countries() > 23:
                    return True
                return False
            elif self.type == 'destroy':
                if len(self.to_conquer) == 0 and len(player.my_countries) > 0:
                    # Winner by destroy is only checked and conquered at each country battle win
                    # This is just the case in which other player destroyed the enemy.
                    # Changes goal and returns False
                    player.goal.type = 'territory24'
                    player.goal.enemy = None
                    world.changed_goal += 1
                    return False
                return False
            else:
                if set(self.to_conquer).issubset(set(player.my_countries.keys())):
                    return True
                return False
        else:
            return False


def draw_n_goals(n, goal_types, enemies):
    continents = generate_continent_goals()
    random.shuffle(continents)
    results = list()
    for i in range(n):
        _type = random.choice(goal_types)
        if _type == 'continent':
            if len(continents) > 0:
                g = Goal(_type)
                g.to_conquer = continents.pop()
            else:
                g = Goal(random.choice(['territory18', 'territory24']))
        elif _type == 'destroy':
            random.shuffle(enemies)
            e = random.choice(enemies, replace=False)
            g = Goal(_type, e)
        else:
            g = Goal(_type)
        results.append(g)
    return results


if __name__ == '__main__':
    # cts = load_data()
    # a = generate_continent_goals()
    # for i in a:
    #     print(i)
    goals = draw_n_goals(6, types, possible_enemies)
    [print(c.to_conquer) for c in goals]
