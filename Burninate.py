import numpy as np
import serial
import time
import random


indata = np.genfromtxt("./NatalieEricFam.csv", dtype = None, delimiter = ",", names = None)
if indata.shape[0] > indata.shape[1]:
    indata = indata.transpose()
#idx = range(indata.shape[1])
#idx.reverse()
#indata = indata[:,idx]


# Max val is 32000
scale_factor = np.max(indata)/32000.0
indata = np.array(indata/scale_factor, dtype = np.int16)
assert(not np.any(indata< 0))



#ser = serial.Serial("/dev/cu.usbmodemfa131",9600, timeout = 100)
#ser = serial.Serial("/dev/cu.usbmodemfa131",57600, timeout = 1)
ser = serial.Serial("/dev/cu.usbmodemfd121",57600, timeout = 1)


print ser.portstr

haveHandshake = False

#currentrw = 0
#currentcol = 0
currentrw =0 
currentcol = 0
cells_burned = 0

row_col_visited = {}
for i in range(indata.shape[0]):
    for j in range(indata.shape[1]):
        if indata[i][j] != 0:
            row_col_visited[str(i) + "," + str(j)] = False
        else:
            row_col_visited[str(i) + "," + str(j)] = True

#visitedfile = open("./AlreadyVisited.txt", "r")
#for i in visitedfile.readlines():
#    if "Advancing" in i:
#        instr = "".join([x for x in i if (x in ",1234567890")])
#        row_col_visited[instr] = True





steps =4
increasing_columnwise = True


def increment6():
    global currentcol
    global currentrw
    global row_col_visited
    draw = increment3()
    if draw == False:
        currentrw = 0
        currentcol = 0
        draw = True
    idx = str(currentrw) + "," + str(currentcol)
    if row_col_visited[idx] == False:
        if random.uniform(0,1) < 0.5:
            return(draw)
        else:
            return(increment6())
    else:
        return(increment6())



def increment5():
    global currentcol
    global currentrw
    global row_col_visited

    draw = increment3()
    idx = str(currentrw) +"," + str(currentcol)
    if row_col_visited[idx] == False:
        return(draw)
    else:
        return(increment5())

def increment4():
    global currentcol
    global currentrw
    global row_col_visited
 
    draw = random.uniform(0,1)
    oldcol = currentcol
    oldrw  = currentrw
    if draw <= 0.25:
        currentcol += 1


        if currentcol < indata.shape[1] and row_col_visited[str(currentrw)+"," + str(currentcol)] == False:
            return(True)
        else:
            currentcol = oldcol
            currentrw = oldrw

            return(increment4())
    elif draw <= 0.5:
        currentcol -= 1


        if currentcol >= 0 and row_col_visited[str(currentrw)+"," + str(currentcol)] == False:
            return(True)
        else:
            currentcol = oldcol
            currentrw = oldrw

            return(increment4())

    elif draw <= 0.75:
        currentrw += 1


        if currentrw < indata.shape[0] and row_col_visited[str(currentrw)+"," + str(currentcol)] == False:
            return(True)
        else:
            currentcol = oldcol
            currentrw = oldrw
            return(increment4())

    elif draw <= 0.99:
        currentrw -= 1

        if currentrw >= 0 and row_col_visited[str(currentrw)+"," + str(currentcol)] == False:

            return(True)
        else:
            currentcol = oldcol
            currentrw = oldrw

            return(increment4())
    else:
        keys = row_col_visited.keys()[:]
        randokeys = random.sample(keys, len(keys))

        for i in randokeys:
            if row_col_visited[i] == False:
                tmp = i.split(",")
                currentrw = int(tmp[0])
                currentcol = int(tmp[1])
                print("Random Draw Made")
                return(True)
        return(False)
    

def increment3():
    global currentcol
    global currentrw
    global steps
    global cellsburned
    global increasing_columnwise
    if increasing_columnwise:
        if currentcol == (indata.shape[1] - 1):
            #end of row
            if currentrw < (indata.shape[0] - 1):
                currentrw += 1
                increasing_columnwise = False
                if (indata[currentrw][currentcol] != 0):
                    return(True)
                else:
                    return(increment3())
            elif currentrw == (indata.shape[0] - 1):
                return(False)
        else:
            currentcol += 1
            if (indata[currentrw][currentcol] != 0):
                return(True)
            else:
                return(increment3())
    else:
        if currentcol == (0):
            #beginning of row
            if currentrw < (indata.shape[0] - 1):
                currentrw += 1
                increasing_columnwise = True
                if (indata[currentrw][currentcol] != 0):
                    return(True)
                else:
                    return(increment3())
            elif currentrw == (indata.shape[0] - 1):
                return(False)
        else:
            currentcol -= 1
            if (indata[currentrw][currentcol] != 0):
                return(True)
            else:
                return(increment3())

def increment2():
    global currentcol
    global currentrw
    global steps
    global cellsburned
    global increasing_columnwise
    if increasing_columnwise:
        if currentcol == (indata.shape[1] - 1):
            #end of row
            if currentrw < (indata.shape[0] - 1):
                currentrw += 1
                increasing_columnwise = False
                return(True)
            elif currentrw == (indata.shape[0] - 1):
                return(False)
        else:
            currentcol += 1
            return(True)
    else:
        if currentcol == (0):
            #beginning of row
            if currentrw < (indata.shape[0] - 1):
                currentrw += 1
                increasing_columnwise = True
                return(True)
            elif currentrw == (indata.shape[0] - 1):
                return(False)
        else:
            currentcol -= 1
            return(True)

def increment():
    global currentcol
    global currentrw
    global steps
    if currentcol == (indata.shape[1] - 1):
        # End of row
        if currentrw < (indata.shape[0]-1):
            currentcol = 0
            currentrw += 1
            print("#########################")
            print("###### NEW COLUMN #######")
            print("#########################")

            return(True)
        # end of doc
        elif currentrw == (indata.shape[0] - 1):
            return(False)
    else:
        currentcol += 1
        return(True)

        
def establishContact():
    global steps
    while(True):
        x = ser.read()
        if x == "A":
            print("Received announce")
            ser.write("A")
            continue
        elif x == ("B"):
            print("Recieved handshake, sending max.")
            ser.write(str(np.max(indata)))
            time.sleep(0.1) 
            x = ser.readline()
            print(x)
            if getChar("X"):
                ser.write(str(indata.shape[1]*steps) + "x")
                print("Sent Max X")
            if getChar("Y"):
                ser.write(str(indata.shape[0]*steps) + "x")
                print("Sent Max Y")
            if getChar("N"):
                print("Maxima received.")


            return(startProgram())

def getChar(char):
    while (True):
        x = ser.read()
        if x == char:
            return(True)
    return(False)

def startProgram():
    print("Starting sequence...")
    global steps
    global currentrw
    global currentcol
    while True:
        if getChar("N"):        
            print("Advancing: row " + str(currentrw) + ", col " + str(currentcol))
            outdata = indata[currentrw][currentcol]
            print("Value: " + str(outdata))
            ser.write(str(outdata) + "x")
            if getChar("X"):
                ser.write(str(currentcol*steps) + "x")
                print("Sent X")
            if getChar("Y"):
                ser.write(str(currentrw*steps) + "x")
                print("Sent Y")
            test = increment3()
            if not test:
                return(True)
                #if cells_burned == np.prod(indata.shape):
                #    return(True)
                #else:
                #    currentrw = 0
                #    currentcol = 0
            else:
                row_col_visited[str(currentrw) + "," + str(currentcol)] = True

            

establishContact()


