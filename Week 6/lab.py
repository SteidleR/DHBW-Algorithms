import copy
import time
import os

labname = ["testlabtheseus.txt", "testlab2.txt", "lab.txt"][0]
stepName = {"U": [0, -1], "D": [0, 1], "R": [1, 0], "L": [-1, 0]}

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
        try:
            path.index(np)
            continue
        except:
            if lab[np[1]][np[0]] != "#":
                nextp.append(key)
    return nextp

def walk(p, step, cost, lab):
    p_new = [p[0] + stepName[step][0], p[1] + stepName[step][1]]
    p_new.append(cost + getCost(p_new, lab))
    return p_new


def checkBetter(x,y, path, solvedPaths, lab, cost):
    worsePaths = []
    lensp = None
    for i in range(len(solvedPaths)):
        sp = solvedPaths[i]
        try:
            #lensp = sp.index([x,y])
            #lenpath = len(path)

            for p in sp:
                if p[:2] == [x,y]:
                    lensp = p[2]
                    break
            if not lensp:
                raise Exception()
            lenpath = cost
            if lenpath > lensp:
                return True, worsePaths
            elif lenpath < lensp:
                worsePaths.append(i)
        except:
            continue
    return False, worsePaths

def checkSnake(p, pp, path):
    for key, val in stepName.items():
        testp = [p[0]+val[0], p[1]+val[1]]
        if testp == pp:
            continue
        try:
            path.index(testp)
            return True
        except:
            continue
    return False

def getCost(p, lab):
    p = lab[p[1]][p[0]]
    if p == " ":
        return 1
    elif p == "S" or p == "X":
        return 1
    else:
        return int(p)

def calcCosts(lab, path):
    costs = 0
    for p in path:
        if p == True:
            break
        currentPoint = lab[p[1]][p[0]]
        if currentPoint == " ":
            costs += 1
        elif currentPoint == "S" or currentPoint == "X":
            costs += 1
        else:
            costs += int(lab[p[1]][p[0]])
    return costs

def solveLab(x, y, lab):
    solvedPaths = []
    currentPath = [[sx,sy]]
    pendingPaths = []
    worsePath = []
    while True:
           cost = 0
        while True:
            # Check if Path is at Endpoint
            if x==ex and y==ey:
                currentPath.append(True)
                solvedPaths.append(currentPath)
                if worsePath:
                    worsePath = list(dict.fromkeys(worsePath))
                    worsePath.sort()
                    for i in worsePath[::-1]:
                        del solvedPaths[i]
                break

            # Get Available steps to walk
            steps = checkNeighbors(currentPath[-1], currentPath[-1 if len(currentPath)==1 else -2], lab, currentPath)
            
            if len(steps) > 1:
                for i in range(1, len(steps)):
                    pendingPaths.append([*currentPath, walk(currentPath[-1][:2], steps[i], cost, lab)])
            elif len(steps)==0:
                break
            [x,y, cost] = walk(currentPath[-1][:2], steps[0], cost, lab)

            # Check if other path is faster
            checkB, wPath = checkBetter(x,y, currentPath, solvedPaths, lab, cost)
            if wPath != []:
                worsePath = [*worsePath, *wPath]
            if checkB:
                break

            # Check if path is snake
            if checkSnake([x,y], currentPath[-1], currentPath):
                break

            currentPath.append([x,y])
        worsePath = []
        if len(pendingPaths):
            currentPath = pendingPaths.pop(0)
            [x,y] = currentPath[-1][:2]
        else:
            break
    return solvedPaths


# ----------------------------------------------------------

if __name__ == "__main__": 
    tstart = time.time()
    lab = readLab(labname)
    paths = solveLab(sx, sy, lab)
    tend = time.time()
    paths.sort(key=lambda s: len(s))
    print("Cost: ", calcCosts(lab, paths[0]))
    printPath(paths[0], lab)
    print("Time needed to solve: ", tend - tstart)