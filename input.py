import sys
#from config import read_config


def read_file():
    """Function reads data from text file and store them in list"""

    #config = read_config()
    sep = " "
    data = []

    #content = sys.stdin.readlines()
    with open("dataset.txt", encoding = "utf-8") as file:
        content = file.readlines()
        for line in content:
            line = line.strip()
            l = line.split(sep)
            if len(l) > 5:
                del l[5:]
            elif len(l) < 4:
                add = [None for i in range(4 - len(l))]
                l = l + add
            for i in range(len(l)):
                if l[i] == ('' or None) and i == 3:
                    l[i] = 1000
                elif l[i] == '' and i != 3:
                    l[i] = None
            if l[3] == 1000 or l[3] == "1000":
                l[3] = 9999
            elif l[3] == "missing":
                l[3] = 1000
            try:
                if l[1] != "S0" and l[3] != 1000:
                    l[3] = int(l[3])
                    l.append(None)
            except ValueError:
                l[3] = 9999
                l.append(None)
            try:
                if l[1] == "S0" and l[3] != 1000:
                    l[3] = int(l[3])
                    l[4] = int(l[4])
            except ValueError:
                l[3] = 9999
                l[4] = 9999
            if l[3] == 1000:
                l.append(None)
            if len(l) > 5:
                del l[5]
            data.append(l)
    return data

read_file()
