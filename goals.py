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

from numpy import random

from countries import data

continent_goals = [['Asia', 'South America'], ['Asia', 'Africa'], ['North America', 'Africa'],
                   ['North America', 'Asia', 'Australia']]
types = ['continent', 'destroy', 'territory18', 'territory24']
possible_enemies = ['black', 'white', 'blue', 'red', 'yellow', 'green']


def generate_continent_goals():
    ctn_goals = list()
    for each in continent_goals:
        to_conquer = list()
        for k, v in data['continent_names'].items():
            if v in each:
                to_conquer += data['continents'][k]
        ctn_goals.append(to_conquer)
    return ctn_goals


continent_countries = generate_continent_goals()


class Goal:
    def __init__(self, _type=None, enemy=None):
        self.type = _type
        self.enemy = enemy
        self.to_conquer = list()

    def update_goal(self, enemy, countries):
        if self.type == 'destroy':
            self.to_conquer = [c for c in countries if c.owner == enemy]

    def check_goal(self, player):
        if self.type == 'territory18':
            if len([c for c in player.my_countries if player.my_countries.army > 1]) > 17:
                return True
            return False
        elif self.type == 'territory24':
            if player.num_countries() > 23:
                return True
            return False
        elif self.type == 'destroy':
            if len(self.to_conquer) == 0:
                return True
            return False
        else:
            conquered = [c.id for c in player.my_countries]
            to_conquer = [c for c in conquered if c in self.to_conquer]
            if len(conquered) >= len(to_conquer):
                return True
            return False


def draw_n_goals(n, goal_types, enemies):
    countries = generate_continent_goals()
    results = list()
    for i in range(n):
        _type = random.choice(goal_types)
        if _type == 'continent':
            if len(countries) > 0:
                random.shuffle(countries)
                c = countries.pop()
                g = Goal(_type)
                g.to_conquer = c
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
    goals = draw_n_goals(6, types, possible_enemies)
