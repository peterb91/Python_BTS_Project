def read_config():
    """Function reads configuration settings in configuration text file and store them in list"""

    separator = " "
    config = []

    with open("config_file.txt") as file:
        content = file.readlines()
        for line in content:
            line = line.strip()
            l = line.split(separator)
            if len(l) < 3:
                l.append("")
                l[2] = None
                config.append(l[2])
            else:
                if l[2] == "":
                    l[2] = None
                    config.append(l[2])
                else:
                    config.append(int(l[2]))
    print(config)
    return config

read_config()
