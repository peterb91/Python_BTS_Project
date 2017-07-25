import logs


def read_file(content):
    """Function reads data from text file and store them in list"""
    sep = " "
    data = []

    logs.logger.info("Starting reading data from input file and storing in a list")

    for line in content:
        line = line.strip()
        l = line.split(sep)
        if len(l) > 5:
            del l[5:]
            logs.logger.info(("remove any data after 5th column: ", l))
        elif len(l) < 4:
            add = [None for i in range(4 - len(l))]
            l = l + add
            logs.logger.info(
                ("adding None value if no value for direction, cell id, terminal id or signal strength", l))
        for i in range(len(l)):
            if l[i] == ('' or None) and i == 3:
                l[i] = 1000
                logs.logger.info(("signal strength is None or no data: insert value: ", l[i], "for", l))
            elif l[i] == '' and i != 3:
                l[i] = None
        if l[3] == 1000 or l[3] == "1000":
            l[3] = 9999
            logs.logger.info(("assign signal strenght = ", l[3], "if signal strenght equals to 1000"))
        elif l[3] == "missing":
            l[3] = 1000
            logs.logger.info(("assign signal strenght = ", l[3], "if signal strenght is missing"))
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
    logs.logger.info("Finishing storing input data to a list\n")
    return data
