from input import read_file

def input_charts():
    inData = read_file()
    msNames = []
    timestamp=0
    # add timestamp to dataset
    for i in inData:
        i.append(timestamp)
        timestamp+=0.5
    # create list with unique MS terminal names
    for i in range(len(inData)):
        if inData[i][2] not in msNames:
            msNames.append(inData[i][2])
    # save data to separate txt files according to MS name
    for ms in msNames:
        with open("ms_" + ms + ".txt", "w") as file:
            for i in inData:
                if i[2] == ms and i[3]!=1000:
                    file.write("%s %s" %(i[5],i[3]))
                    file.write("\n")
                else:
                    file.write("\n")
        # if there is some missing data save measurements in separate txt file
        with open("missing_" + ms + ".txt", "w") as file:
            for i in inData:
                if i[2] == ms and i[3]==1000:
                    file.write("%s %d" %(i[5],0))
                    file.write("\n")

