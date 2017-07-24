import sys


def read_file():
    sep = " "
    data = []

    #content = sys.stdin.readlines()
    with open("dataset.txt", encoding = 'utf-8') as file:
        content = file.readlines()
        for line in content:
            line = line.strip()
            l = line.split(sep)
            if len(l) < 4:
                add = [None for i in range(4 - len(l))]
                l = l + add
            for i in range(len(l)):
                if l[i] == ('' or None) and i == 3:
                    l[i] = 1000
                elif l[i] == '' and i != 3:
                    l[i] = None
            if l[3] == "missing":
                l[3] = 1000
            if l[1] != "S0" and l[3] != 1000:
                l[3] = int(l[3])
                l.append(None)
            elif l[1] == "S0" and l[3] != 1000:
                l[3] = int(l[3])
                l[4] = int(l[4])
            elif l[3] == 1000:
                l.append(None)
<<<<<<< HEAD
            data.append(l)
        print(l)
=======
            data.append(l),
        #for i in data:
            #print (i), "\n"
>>>>>>> b86f56119b5957535f131512f16936105362b6bc
    return data
read_file()
