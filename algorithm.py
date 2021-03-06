from config import read_config
from os import write

outputData = []
terminals = {}
missings = {}
quality = {}
lastWorked = {}
lastNeighbour = {}

configs = read_config()

target = configs[0]
hysteresis = configs[1]
maxInc = configs[2]
maxDec = configs[3]
values = configs[4]
missing = configs[5]


def avg_qual(numbers):
    """Calculates weighted average"""
    up = 0
    down = 0
    mul = 1
    for i in reversed(numbers):
        up += i * mul
        down += mul
        mul /= 2
    return up/down


def avg(numbers):
    """Calculates weighted average and subtracts it from target SS"""
    result = avg_qual(numbers)
    return target - result


def power_management(data):
    """Changes list of read data into list of results calculating expected by power management for BTS requirements"""
    for i in data:
        missed = False  # Signal may come back, we check it later if its missed
        if i[3] == 1000:  # Given value (from readData from input.py) 1000 means that our signal is missing
            missed = True
            if i[0] in ["UL", "DL"] and i[1] == "S0" and i[4] is None:  # Checks if values are proper
                if i[0] + i[2] not in missings:  # Adds missing signal if it wasn't in the dictionary
                    missings[i[0] + i[2]] = 1
                elif missings[i[0] + i[2]] < missing:  # Increments number of missing signals before it reaches maximum
                    missings[i[0] + i[2]] += 1
                    i[3] = lastWorked[i[0] + i[2]]
                    i[4] = 5
                else:
                    i[3] = -95
                    i[4] = 5
        if(i[0] not in["UL", "DL"] or i[1] not in ["S0", "N1", "N2", "N3", "N4", "N5", "N6"] or i[3] < -95 or i[3] > -45
           or i[4] not in [0, 1, 2, 3, 4, 5]):  # Checks data correctness, if wrong gives error code (0) into output
            outputData.append([0])
        elif i[1] == "S0":  # Seeks for expected terminal S0
            if not missed:
                missings[i[0] + i[2]] = 0  # Resets missing counter if our signal came back
            inserted = False
            if i[0] + i[2] not in terminals:
                terminals[i[0] + i[2]] = [i[3]]  # Adds new UL/DL terminals signals strength
                quality[i[0] + i[2]] = [i[4]]  # and qualities into dictionary for later use
                inserted = True
                if values > 1:  # Only if values to check is more than 1 we append No Change instruction
                    outputData.append([i[0], i[1], i[2], "NCH", None])
                    write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  NCH\n").encode("utf-8"))
            if not inserted or values == 1:  # Checks if event is able to calculate
                if not inserted:
                    terminals[i[0] + i[2]].append(i[3])  # If before weren't add signal strength
                    quality[i[0] + i[2]].append(i[4])  # and quality into dictionary for later use
                if len(terminals[i[0] + i[2]]) >= values:  # Checks if event is able to calculate
                    deviation = avg(terminals[i[0] + i[2]][-values:])
                    qual = avg_qual(quality[i[0] + i[2]][-values:])
                    if abs(deviation) >= 1 and qual < 4:  # Checks if we should change signal normally
                        if deviation < 0:  # Decrease signal
                            if qual < 2:  # Checks if we can decrease signal
                                if abs(deviation) < hysteresis:
                                    outputData.append([i[0], i[1], i[2], "DEC", 1])
                                    write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  DEC  1\n").encode("utf-8"))
                                elif abs(deviation) >= maxDec:
                                    outputData.append([i[0], i[1], i[2], "DEC", maxDec])
                                    write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  DEC  " +\
                                              str(maxDec) + "\n").encode("utf-8"))
                                else:
                                    outputData.append([i[0], i[1], i[2], "DEC", -int(round(deviation))])
                                    write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  DEC  " +\
                                              str(-int(round(deviation))) + "\n").encode("utf-8"))
                            else:
                                outputData.append([i[0], i[1], i[2], "NCH", None])
                                write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  NCH\n").encode("utf-8"))
                        elif deviation > 0:  # Increase signal
                            if abs(deviation) < hysteresis:
                                outputData.append([i[0], i[1], i[2], "INC", 1])
                                write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  INC  1\n").encode("utf-8"))
                            elif abs(deviation) >= maxInc:
                                outputData.append([i[0], i[1], i[2], "INC", maxInc])
                                write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  INC  " + str(maxInc) +\
                                          "\n").encode("utf-8"))
                            else:
                                outputData.append([i[0], i[1], i[2], "INC", int(round(deviation))])
                                write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  INC  " + str(int(round(deviation))) +\
                                          "\n").encode("utf-8"))
                    elif qual >= 4:  # Very low quality (high value) means increase
                        if int(deviation) > 2:  # If more than minimum value we use normal algorithm
                            if int(deviation) >= maxInc:
                                outputData.append([i[0], i[1], i[2], "INC", maxInc])
                                write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  INC  " +\
                                          str(maxInc) + "\n").encode("utf-8"))
                            else:
                                outputData.append([i[0], i[1], i[2], "INC", int(round(deviation))])
                                write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  INC  " +\
                                          str(int(round(deviation))) + "\n").encode("utf-8"))
                        else:  # If less we use minimum value (2)
                            outputData.append([i[0], i[1], i[2], "INC", 2])
                            write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  INC  2" + "\n").encode("utf-8"))
                    else:  # If deviation is less than given hysteresis there is no change to signal
                        outputData.append([i[0], i[1], i[2], "NCH", None])
                        write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  NCH\n").encode("utf-8"))
                    if i[0] + i[2] in lastNeighbour:
                        mini = list(lastNeighbour[i[0] + i[2]].values())[0]
                        neigh = list(lastNeighbour[i[0] + i[2]].keys())[0]
                        for a in lastNeighbour[i[0] + i[2]]:
                            if int(lastNeighbour[i[0]+i[2]][a]) > mini:
                                mini = int(lastNeighbour[i[0]+i[2]][a])
                                neigh = a
                        if mini > 3 + int(round(avg_qual(terminals[i[0] + i[2]][-values:]))):
                            write(1, (i[0] + "  " + neigh + "  " + i[2] + "  HOBC\n").encode("utf-8"))
                else:  # If there is not enough signals to calculate we don't send change command
                    outputData.append([i[0], i[1], i[2], "NCH", None])
                    write(1, (i[0] + "  " + i[1] + "  " + i[2] + "  NCH\n").encode("utf-8"))
            lastWorked[i[0] + i[2]] = i[3]  # We add last working signal into dictionary in case of missing signal
        if i[0] == "DL" and i[1] in ["N1", "N2", "N3", "N4", "N5", "N6"] and not (i[3] < -95 or i[3] > -45):
                if i[0] + i[2] in lastNeighbour.keys():
                    lastNeighbour[i[0] + i[2]].update({i[1]: i[3]})
                else:
                    lastNeighbour[i[0] + i[2]] = ({i[1]: i[3]})
                if i[0] + i[2] in terminals:
                    if len(terminals[i[0] + i[2]]) >= values:
                        mini = list(lastNeighbour[i[0] + i[2]].values())[0]
                        neigh = list(lastNeighbour[i[0] + i[2]].keys())[0]
                        for a in lastNeighbour[i[0] + i[2]]:
                            if int(lastNeighbour[i[0] + i[2]][a]) > mini:
                                mini = int(lastNeighbour[i[0] + i[2]][a])
                                neigh = a
                        if mini > 3 + int(round(avg_qual(terminals[i[0] + i[2]][-values:]))):
                            write(1, (i[0] + "  " + neigh + "  " + i[2] + "  HOBC\n").encode("utf-8"))
    return outputData
