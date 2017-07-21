from data_generator import random_data
from input import read_file
from SaveOutputTxt import writeToTxt

'''data = [["DL", "S0", "MS776", -78, 1],\
 ["DL", "S0", "MS776", -82, 1],\
 ["DL", "S0", "MS776", -87, 1],\
 ["DL", "S0", "MS776", -85, 1],\
 ["UL", "S0", "MS222", -70, 1],\
 ["DL", "N1", "MS222", -65, None],\
 ["UL", "S0", "MS455", -999, 3]]'''

random_data(200)
data = read_file()

outputData = []
terminals = {}
missings = {}
lastWorked = {}

target = -75
hysteresis = 3
maxInc = 8
maxDec = 4
values = 2
missing = 3
index = 0


def avg(numbers):
    up = 0
    down = 0
    mul = 1
    for i in reversed(numbers):
        up += i * mul
        down += mul
        mul /= 2
    return int(target - (up/down))


def power_management():
    for i in data:
        missed = False
        if i[3] == 1000:
            missed = True
            if i[0] in ["UL", "DL"] and i[1] == "S0" and i[4] is None:
                if i[0] + i[2] not in missings:
                    missings[i[0] + i[2]] = 1
                elif missings[i[0] + i[2]] <= missing:
                    missings[i[0] + i[2]] += 1
                    i[3] = lastWorked[i[0] + i[2]]
                    i[4] = 5
                else:
                    i[3] = -95
                    i[4] = 5
        if(i[0] not in["UL", "DL"] or i[1] not in ["S0", "N1", "N2", "N3", "N4", "N5", "N6"] or i[3] < -95 or i[3] > -45\
               or i[4] not in [0, 1, 2, 3, 4, 5]):
            outputData.append([0])
        elif i[1] == "S0":
            if not missed:
                missings[i[0] + i[2]] = 0
            if i[0] + i[2] in terminals:
                terminals[i[0] + i[2]].append(i[3])
                if len(terminals[i[0] + i[2]]) >= values:
                    deviation = avg(terminals[i[0] + i[2]][-values:])
                    if abs(deviation) > hysteresis and i[4] < 4:
                        if deviation < 0:
                            if abs(deviation) >= maxDec and i[4] < 2:
                                outputData.append([i[0], i[1], i[2], "DEC", maxDec])
                            elif i[4] < 2:
                                outputData.append([i[0], i[1], i[2], "DEC", -deviation])
                            else:
                                outputData.append([i[0], i[1], i[2], "NCH", None])
                        elif deviation > 0:
                            if abs(deviation) >= maxInc:
                                outputData.append([i[0], i[1], i[2], "INC", maxInc])
                            else:
                                outputData.append([i[0], i[1], i[2], "INC", deviation])
                    elif abs(deviation) > hysteresis and i[4] >= 4:
                        if deviation > 2:
                            if abs(deviation) >= maxInc:
                                outputData.append([i[0], i[1], i[2], "INC", maxInc])
                            else:
                                outputData.append([i[0], i[1], i[2], "INC", deviation])
                        else:
                            outputData.append([i[0], i[1], i[2], "INC", 2])
                    else:
                        outputData.append([i[0], i[1], i[2], "NCH", None])
                else:
                    outputData.append([i[0], i[1], i[2], "NCH", None])

            else:
                terminals[i[0] + i[2]] = [i[3]]
                outputData.append([i[0], i[1], i[2], "NCH", None])
            lastWorked[i[0] + i[2]] = i[3]

    return outputData

power_management()

writeToTxt(outputData)
#print(outputData)
