import copy
import time
import os

labname = ["testlabtheseus.txt", "testlab2.txt", "lab.txt", "lab_big.txt"][2]
stepName = {"U": [0, -1], "D": [0, 1], "R": [1, 0], "L": [-1, 0], "UR": [1, -1], "UL": [-1, -1], "DR": [1, 1], "DL": [-1, 1]}
def readLab(fname):
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
    return arr, [sx, sy], [ex, ey]

def printLab(arr):
    for l in arr:
        print("".join(l))

def printPath(path, lab):
    for i in range(1, len(path)-1):
        p = path[i]
        lab[p[1]][p[0]] = "\u001b[47m\u001b[34m{}\u001b[0m".format(lab[p[1]][p[0]])
    printLab(lab)

def calculateCost(path, lab):
    cost = 0
    for p in path:
        char = lab[p[1]][p[0]]
        if char == " ":
            cost += 1
        elif char == "S" or char == "X":
            cost += 1
        elif char in "0123456789":
            cost += int(char)
        else:
            raise ValueError("An unknown Cost is found!")
    return cost

# ----------- Functions to solve the Lab ----------------

def checkNeighbours(p, pp, lab, path):
    x = p[0]
    y = p[1]
    px = pp[0]
    py = pp[1]
    nextp = []
    for key, val in stepName.items():
        np = [x+val[0], y+val[1]]
        if lab[np[1]][np[0]] == "#":
            continue
        elif np == pp:
            continue
        
        elif np in path:
            return None
        
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
            steps = checkNeighbours(point, currentPath[-2 if len(currentPath)>1 else -1], lab, currentPath)
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
    lab, sp, ep  = readLab(labname)
    paths = solve(lab, sp, ep)
    tend = time.time()
    paths.sort(key= lambda i: calculateCost(i, lab))
    cost = calculateCost(paths[0], lab)
    printPath(paths[0], lab)   
    print("Cost: ",cost)
    print("Time needed to solve: ", tend - tstart)