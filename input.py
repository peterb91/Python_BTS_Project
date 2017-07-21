import database


def read_file():

    sep = " "
    data = []

    with open("dataset.txt") as file:
        content = file.readlines()
    for line in content:
        line = line.strip()
        if line[:2] in ('DL', 'UL'):
            l = line.split(sep)
            if l[1] not in 'S0' and l[3] not in 'missing':
                l[3] = int(l[3])
                l.append('None')
            elif l[1] in 'S0' and l[3] not in 'missing':
                l[3] = int(l[3])
                l[4] = int(l[4])
            elif l[3] in 'missing':
                l.append('None')
            #print(l)
            data.append(l)
        #else:
            #l = [incorrect, incorrect, incorrect, incorrect, incorrect]
            #data.append(l)'''
    archiver = database.DatabaseArchiver('/tmp/BTStest.db')
    archiver.save_measurement(data)
    return data

read_file()
