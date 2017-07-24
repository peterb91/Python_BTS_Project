import random


def random_data (amount):
    """Function generates pseudo random data for input"""

    with open("dataset.txt", "w+") as file:
        links = ["UL", "UL", "UL", "UL", "DL", "DL", "DL", "DL", "SL"]
        terminals = ["S0", "S0", "S0", "S0", "S0", "S0", "S0", "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "S1"]
        stations = ["MS776", "MS222", "MS543", "MS754"]
        strength = [i for i in range(-99, -95, 2)] + [i for i in range(-95, -45, 1)] + [i for i in range(-45, -10, 8)]\
                   + ["missing"]  # generates irreguar list of numbers from -99 to -10
        for i in range(amount):
            col1 = random.choice(links)
            col2 = random.choice(terminals)
            col3 = random.choice(stations)
            col4 = random.choice(strength)
            if col2 in "S0" and str(col4) not in "missing":
                col5 = random.randint(1, 5)
            else:
                col5 = ""
            file.write("%s %s %s %s %s\n" %(col1, col2, col3, col4, col5))

