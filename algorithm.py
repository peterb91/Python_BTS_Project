from data_generator import random_data
from input import read_file
from SaveOutputTxt import writeToTxt
from config import read_config

#random_data(20000)
data = read_file()

outputData = []
terminals = {}
missings = {}
quality = {}
lastWorked = {}

configs = read_config()

target = configs[0]
hysteresis = configs[1]
maxInc = configs[2]
maxDec = configs[3]
values = configs[4]
missing = configs[5]


def avg(numbers):
    """Calculates weighted average"""
    up = 0
    down = 0
    mul = 1
    for i in reversed(numbers):
        up += i * mul
        down += mul
        mul /= 2
    return int(target - (up/down))


def power_management():
    """Changes list of read data into list of results calculating expected by power management for BTS requirements"""
    for i in data:
        missed = False #Signal may come back, we check it later if its missed
        if i[3] == 1000: #Given value (from readData from input.py) 1000 means that our signal is missing
            missed = True
            if i[0] in ["UL", "DL"] and i[1] == "S0" and i[4] is None: #Checks if values are proper
                if i[0] + i[2] not in missings: #Adds missing signal if it wasn't in the
                    missings[i[0] + i[2]] = 1
                elif missings[i[0] + i[2]] <= missing: #Increments number of missing signals before it reaches maximum
                    missings[i[0] + i[2]] += 1
                    i[3] = lastWorked[i[0] + i[2]]
                    i[4] = 5
                else:
                    i[3] = -95
                    i[4] = 5
        if(i[0] not in["UL", "DL"] or i[1] not in ["S0", "N1", "N2", "N3", "N4", "N5", "N6"] or i[3] < -95 or i[3] > -45\
               or i[4] not in [0, 1, 2, 3, 4, 5]): #Checks data correctness, if wrong gives error code (0) into output
            outputData.append([0])
        elif i[1] == "S0": #Seeks for expected terminal S0
            if not missed:
                missings[i[0] + i[2]] = 0 #Resets missing counter if our signal came back
            inserted = False
            if i[0] + i[2] not in terminals:
                terminals[i[0] + i[2]] = [i[3]]
                quality[i[0] + i[2]] = [i[4]]
                inserted = True
                if values > 1:
                    outputData.append([i[0], i[1], i[2], "NCH", None])
                    print(i[0], i[1], i[2], "NCH")
            if not inserted or values == 1:
                if not inserted:
                    terminals[i[0] + i[2]].append(i[3])
                    quality[i[0] + i[2]].append(i[4])
                if len(terminals[i[0] + i[2]]) >= values:
                    deviation = avg(terminals[i[0] + i[2]][-values:])
                    qual = avg(quality[i[0] + i[2]][-values:])
                    if abs(deviation) > hysteresis and qual < 4:
                        if deviation < 0:
                            if abs(deviation) >= maxDec and qual < 2:
                                outputData.append([i[0], i[1], i[2], "DEC", maxDec])
                                print(i[0], i[1], i[2], "DEC", maxDec)
                            elif qual < 2:
                                outputData.append([i[0], i[1], i[2], "DEC", -deviation])
                                print(i[0], i[1], i[2], "DEC", -deviation)
                            else:
                                outputData.append([i[0], i[1], i[2], "NCH", None])
                                print(i[0], i[1], i[2], "NCH")
                        elif deviation > 0:
                            if abs(deviation) >= maxInc:
                                outputData.append([i[0], i[1], i[2], "INC", maxInc])
                                print(i[0], i[1], i[2], "INC", maxInc)
                            else:
                                outputData.append([i[0], i[1], i[2], "INC", deviation])
                                print(i[0], i[1], i[2], "INC", deviation)
                    elif abs(deviation) > hysteresis or qual >= 4:
                        if abs(deviation) > 2:
                            if abs(deviation) >= maxInc:
                                outputData.append([i[0], i[1], i[2], "INC", maxInc])
                                print(i[0], i[1], i[2], "INC", maxInc)
                            else:
                                outputData.append([i[0], i[1], i[2], "INC", deviation])
                                print(i[0], i[1], i[2], "INC", deviation)
                        else:
                            outputData.append([i[0], i[1], i[2], "INC", 2])
                            print(i[0], i[1], i[2], "INC", 2)
                    else:
                        outputData.append([i[0], i[1], i[2], "NCH", None])
                        print(i[0], i[1], i[2], "NCH")
                else:
                    outputData.append([i[0], i[1], i[2], "NCH", None])
                    print(i[0], i[1], i[2], "NCH")
            lastWorked[i[0] + i[2]] = i[3]
    return outputData

power_management()
writeToTxt(outputData)
