import logs


def input_charts(content):
    logs.logger.info("Starting writing data for chart creation ")
    in_data = content
    ms_names = []
    timestamp = 0
    logs.logger.info("adding timestamp to dataset")
    # add timestamp to dataset
    for i in in_data:
        i.append(timestamp)
        timestamp += 0.5
    # create list with unique MS terminal names
    for i in range(len(in_data)):
        if in_data[i][2] not in ms_names:
            ms_names.append(in_data[i][2])
    # save data to separate txt files according to MS name
    for ms in ms_names:
        with open("ms_" + ms + ".txt", "w") as file:
            logs.logger.info(("save data to a file ms_" + ms + ".txt"))
            for i in in_data:
                if i[2] == ms and i[3] != 1000:
                    file.write("%s %s" % (i[5], i[3]))
                    file.write("\n")
                else:
                    file.write("\n")
        # if there is some missing data save measurements in separate txt file
        with open("missing_" + ms + ".txt", "w") as file:
            logs.logger.info(("save data if some missing measurements occurred to a file missing_" + ms + ".txt"))
            for i in in_data:
                if i[2] == ms and i[3] == 1000:
                    file.write("%s %d" % (i[5], 0))
                    file.write("\n")
    logs.logger.info("Finishing writing data for chart creation")
