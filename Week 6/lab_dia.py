import copy
import time
import os

labname = "testlabtheseus.txt"
stepName = {"U": [0, -1], "D": [0, 1], "R": [1, 0], "L": [-1, 0], "UR": [1, -1], "UL": [-1, -1], "DR": [1, 1], "DL": [-1, 1]}

# Coords of Startpoint
sx = None
sy = None

# Coords of Endpoint
ex = None
ey = None

def readLab(fname):
    global sx, sy, ex, ey
    arr = []
    count = 0
    with open(fname) as f:
        for line in f:
            if "S" in line:
                sx = line.index("S")
                sy = count
            if "X" in line:
                ex = line.index("X")
                ey = count
            arr.append(list(line.replace("\n", "")))
            count += 1
    return arr

def printLab(arr):
    for l in arr:
        print("".join(l))

def printPath(path, labn):
    for i in range(1, len(path)-2):
        p = path[i]
        labn[p[1]][p[0]] = "."
    printLab(labn)



# ----------- Functions to solve the Lab ----------------

def checkNeighbors(p, pp, lab, path):
    x = p[0]
    y = p[1]
    px = pp[0]
    py = pp[1]
    nextp = []
    for key, val in stepName.items():
        np = [x+val[0], y+val[1]]
        if px-val[0] == x and py-val[1] == y:
            continue
        elif np in path:
            continue
        elif lab[np[1]][np[0]] != "#":
            nextp.append(key)
    return nextp

def walk(p, step):
    p_new = [p[0] + stepName[step][0], p[1] + stepName[step][1]]
    return p_new


def checkBetter(x,y, path, solvedPaths):
    for sp in solvedPaths:
        s = set(sp)
        if [x,y] in s:
            if len(path) > len(sp[:sp.index([x,y])]):
                return True
    return False

def checkSnake(p, pp, path):
    for key, val in stepName.items():
        testp = [p[0]+val[0], p[1]+val[1]]
        if testp == pp:
            continue
        try:
            path.index(testp)
            return True
        except:
            pass
            
    return False

def calculateCost(path):
    return len(path)

def solveLab(x, y, lab):
    solvedPaths = []
    currentPath = [[sx,sy]]
    pendingPaths = []
    while True:
        while True:
            # Check if Path is at Endpoint
            if x==ex and y==ey:
                currentPath.append(True)
                solvedPaths.append(currentPath)
                break

            # Get Available steps to walk
            steps = checkNeighbors(currentPath[-1], currentPath[-1 if len(currentPath)==1 else -2], lab, currentPath)
            
            if len(steps) > 1:
                for i in range(1, len(steps)):
                    pendingPaths.append([*currentPath, walk(currentPath[-1], steps[i])])
            elif len(steps)==0:
                break
            [x,y] = walk(currentPath[-1], steps[0])

            # Check if other path is faster
            if checkBetter(x,y, currentPath, solvedPaths):
                break
            if checkSnake([x,y], currentPath[-1], currentPath):
                break

            currentPath.append([x,y])
        if len(pendingPaths):
            currentPath = pendingPaths.pop(0)
            [x,y] = currentPath[-1]
        else:
            break
    return solvedPaths


# ----------------------------------------------------------

if __name__ == "__main__": 
    tstart = time.time()
    lab = readLab(labname)
    paths = solveLab(sx, sy, lab)
    print(len(paths))
    paths.sort(key=lambda s: len(s))
    printPath(paths[0], lab)
    tend = time.time()
    print("Time needed to solve: ", tend - tstart)