from countries import data


def deploy(world):
    if world.turn == 0:
        i = 0
        i_max = len(world.countries)
        while i < i_max:
            for p in world.players:
                p.add_country(world.countries[i])
                i += 1
    return world


def full_continent(player):
    armies = dict()
    cts = [str(x.id) for x in player.my_countries]
    for k, v in data['continents'].items():
        if set(v).issubset(cts):
            armies[k] = data['continent_values'][k]
    return armies


def calculate_army(player):
    armies = full_continent(player)
    armies['general'] = player.num_countries() // 2


def make_move(player, turn):
    # get army
    # deployment
    # attack
    # win?
    pass


if __name__ == '__main__':
    pass
