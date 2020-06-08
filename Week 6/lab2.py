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
    for i in range(1, len(path)-1):
        p = path[i]
        labn[p[1]][p[0]] = "."
    printLab(labn)

# ----------- Functions to solve the Lab ----------------

def checkNeighbours(p, pp, lab, path):
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
                nextp.append(np)
    return nextp

def solve(lab, sp, ep):
    solvedPaths = []
    towalkPaths = []
    currentPath = [sp]
    point = sp
    while True:
        while True:
            steps = checkNeighbours(point, currentPath[-1], lab, currentPath)
            if not steps:
                break
            point = steps.pop(0)
            for step in steps:
                towalkPaths.append([*currentPath, step])
            currentPath.append(point)
            if point == ep:
                solvedPaths.append(currentPath)
                break
            if point in currentPath[:-1]:
                break
        
        if towalkPaths:
            currentPath = towalkPaths.pop()
            point = currentPath[-1]
        else:
            break
    return solvedPaths

if __name__ == "__main__":
    tstart = time.time()
    lab  = readLab(labname)
    paths = solve(lab, [sx,sy], [ex,ey])
    tend = time.time()
    paths.sort(key= lambda i: len(i))
    printPath(paths[0], lab)   
    print("Time needed: ", tend - tstart)