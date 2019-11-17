

class Player:
    def __init__(self, id, name, strategy):
        self.id = id
        self.name = name
        self.strategy = strategy
        self.goal = None
        self.my_countries = list()

    def add_country(self, country):
        self.my_countries.append(country)

    def remove_country(self, country):
        self.my_countries.remove(country)

    def num_countries(self):
        return len(self.my_countries)


if __name__ == '__main__':
    p1 = Player(0, 'black', 0)
