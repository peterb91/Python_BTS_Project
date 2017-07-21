#import sys


def read_file():
    sep = " "
    data = []

    #file = sys.stdin
    with open("dataset.txt") as file:
        content = file.readlines()
        for line in content:
            line = line.strip()
            l = line.split(sep)
            if l[3] in "missing":
                l[3] = 1000
            if l[1] not in "S0" and l[3] != 1000:
                l[3] = int(l[3])
                l.append("None")
            elif l[1] in "S0" and l[3] != 1000:
                l[3] = int(l[3])
                l[4] = int(l[4])
            elif l[3] == 1000:
                l.append("None")
        data.append(l)
    return data

read_file()
