from esnap7 import easyPLC
import numpy as np
import datetime as dt
# inputs
#byte 0
S0 = 0 # nødstopp
B1 = 1 # Den øverste sensoren i tanken
B2 = 2 # Sensor 20 cm under B1
B3 = 3 # Sensoren 20 cem over B4
B4 = 4 # Den nederste sensoren i tanken
S1 = 5 # start
S2 = 6 # stopp
F1 = 7 # termisk vern for motor 1
#byte 1
F2 = 0 # termisk vern for motor 2
# outputs
#byte 0
Q1 = 0 # Kontaktor for motor 1
Q2 = 1 # Kontaktor for motor 1
P0 = 5 # Lampe for nødstopp
P1 = 2 # Lampe for drift av pumper
P2 = 6 # Lampe for pause
P3 = 7 # Lampe for alarm

ut = True

pumpeNr = 1

pls = easyPLC.PLC()

dataFile = "data.npy"

try:
    data = np.load(dataFile, allow_pickle='TRUE').item()
except:
    np.save(dataFile, {1: 0, 2: 0})

hours = np.load(dataFile, allow_pickle='TRUE').item()


while True: # koble til PLS
    try:
        pls.begin("192.168.0.1", 0, 1)
    except:
        pass
    else:
        break

while True: # main loop
    listIn = pls.readBoolTag(0, "I")
    listIn1 = pls.readBoolTag(1, "I")
    if S0 in listIn:
        pls.writeBoolTag("Q", 0, P0, True)
        pls.writeBoolTag("Q", 0, Q1, False)
        pls.writeBoolTag("Q", 0, Q2, False)
        pls.writeBoolTag("Q", 0, P1, False)
        pls.writeBoolTag("Q", 0, P0, True)
        print("S0 in lisitin")
        if easyPLC.ifor(listIn, [F1, F2]) == False:
            pls.writeBoolTag("Q",0,P3,True)
            print("Alarm")

    else:
        if easyPLC.ifand(listIn, [F1, F2]) == False:
            if easyPLC.ifor(listIn, [B1, B2]) and easyPLC.ifor(listIn, [B3, B4]) == False:
                if S1 in listIn and ut:
                    if F1 not in listIn:
                        print(2)
                        pumpeNr = 2
                        timeStart = dt.datetime.now()
                        pls.writeBoolTag("Q", 0, Q2, True)
                        pls.writeBoolTag("Q", 0, P1, True)
                        pls.writeBoolTag("Q", 0, P2, False)
                        ut = False

                    elif F2 not in listIn1:
                        print(12)
                        pumpeNr = 1
                        timeStart = dt.datetime.now()
                        pls.writeBoolTag("Q", 0, Q1, True)
                        pls.writeBoolTag("Q", 0, P1, True)
                        pls.writeBoolTag("Q", 0, P2, False)
                        ut = False

                    if hours.get(1) > hours.get(2):
                        print(1)
                        pumpeNr = 1
                        timeStart = dt.datetime.now()
                        pls.writeBoolTag("Q", 0, Q1, False)
                        pls.writeBoolTag("Q", 0, P1, True)
                        pls.writeBoolTag("Q", 0, P2, False)
                        ut = False

                    elif hours.get(1) <= hours.get(2):
                        print(22)
                        pumpeNr = 2
                        timeStart = dt.datetime.now()
                        pls.writeBoolTag("Q", 0, Q2, True)
                        pls.writeBoolTag("Q", 0, P1, True)
                        pls.writeBoolTag("Q", 0, P2, False)
                        ut = False

            if easyPLC.ifor(listIn, [B3, B4, S2]) and ut == False:
                timeEnd = dt.datetime.now()
                time = timeStart - timeEnd
                time = time.total_seconds() / 60 / 60 # getting time in hours
                hours[pumpeNr] == hours.get(pumpeNr) + time
                print(time, hours)
                pls.writeBoolTag("Q", 0, Q1, False)
                pls.writeBoolTag("Q", 0, Q2, False)
                pls.writeBoolTag("Q", 0, P1, False)
                pls.writeBoolTag("Q", 0, P2, True)
                ut = True

                if easyPLC.ifor(listIn, [B1, B2]): #skjekke om sensorer er ødelagt
                    pass

    if S0 not in listIn:
        pls.writeBoolTag("Q", 0, P0, False)

    if easyPLC.ifor(listIn, [F1, F2]):
        pls.writeBoolTag("Q", 0, P3, False)
    else:
        pls.writeBoolTag("Q", 0, P3, True)



