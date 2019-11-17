

class Player:
    def __init__(self, _id):
        self.id = _id
        self.name = None
        self.strategy = None
        self.goal = None
        self.my_countries = list()

    def add_country(self, country):
        self.my_countries.append(country)

    def remove_country(self, country):
        self.my_countries.remove(country)

    def num_countries(self):
        return len(self.my_countries)

    def full_continent(self):
        pass


if __name__ == '__main__':
    p1 = Player(0)
