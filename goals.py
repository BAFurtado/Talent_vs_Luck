''' #  https://boardgamegeek.com/thread/60929/mission-cards

i) Kill a certain colour. There are 6 of these, one for each colour. If fewer than 6 colours are going to be used in the game then the cards corresponding to the unused colours are removed from the deck before missions are given out. (This is quite clearly stated in at least some versions of the rules, and failing to do so doesn't make much sense.) If you draw your own colour, then your mission changes to mission (iv).

ii) Conquer some combination of continents. There are 6 of these:

Conquer Asia and South America;
Conquer Asia and Africa;
Conquer North America and Africa;
Conquer North America and Australasia;
Conquer Europe and South America and a 3rd continent of your choice [this mission is omitted from 1998 US edition];
Conquer Europe and Australasia and a 3rd continent of your choice [this mission is omitted from 1998 US edition].

iii) Occupy 18 territories with at least 2 armies in each territory.

iv) Occupy 24 territories (no restriction to 2 or more armies in each). '''

from countries import load_data, data

continent_goals = [['Asia', 'South America'], ['Asia', 'Africa'], ['North America', 'Africa'],
                   ['North America', 'Asia', 'Australia']]


class Goals:
    def __init__(self):
        self.type = None
        self.to_conquer = list()

    def update_goal(self):
        pass

    def check_goal(self):
        pass


def generate_continent_goals():
    goals = list()
    for each in continent_goals:
        to_conquer = list()
        for k, v in data['continent_names'].items():
            if v in each:
                to_conquer += data['continents'][k]
        goals.append(to_conquer)
    return goals


goals1 = generate_continent_goals()
goals_types = ['continent', 'destroy', 'territory18', 'territory24']


if __name__ == '__main__':
    # cts = load_data()
    for i in goals1:
        print(len(i))
