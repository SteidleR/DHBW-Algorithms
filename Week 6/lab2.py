app_info = {
"Title": "Lab Solver",
"ShortSum": "Solves a lab readed from file",
"LongDescr": "Solves a labyrinth using the Depth-First Search algorithm. Labyrinth is readed from a file. Walls of the labyrinth are #",
"Author": "Robin Steidle",
"Version": "0.5",
"LastEdit": "09.06.2020"
}

import time
import os

# Available test labyrinths to solve
labname = ["testlabtheseus.txt", "testlab2.txt", "lab.txt", "lab_big.txt"][2]
stepName = {"U": [0, -1], "D": [0, 1], "R": [1, 0], "L": [-1, 0]}

def readLab(fname):
    """
    Reads the Labyrinth from file

    :param fname: File name of the labyrinth
    :return:      2D array storing the labyrinth
                  Start Point [x,y]
                  End Point [x,y]
    """
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

def printLab(lab):
    """
    Prints the labyrinth to the screen

    :param lab: 2D Array storing the lab
    """
    for l in lab:
        print("".join(l))

def printPath(path, lab):
    """
    Adds the given Path to the labyrinth array

    :param path: path to print
    :param lab:  2D Array storing the Lab
    """
    for i in range(len(path)):
        p = path[i]
        lab[p[1]][p[0]] = "\u001b[47m\u001b[34m{}\u001b[0m".format(lab[p[1]][p[0]])
    printLab(lab)

def calculateCost(path, lab):
    """
    Calculates the Cost for a path in the labyrinth

    :param path: path to calculate the cost
    :param lab:  2D Array storing the lab
    """
    cost = 0
    for p in path:
        char = lab[p[1]][p[0]]
        if char == " ":
            cost += 1
        elif char == "S" or char == "X":
            cost += 1
        elif char in "0123456789":
            cost += int(char)
    return cost


# ----------- Functions to solve the Lab ----------------

def checkNeighbours(p, pp, lab, path):
    """
    Checks all available points to walk from current point

    :param p:    current point
    :param pp:   previous point
    :param lab:  labyrinth
    :param path: current path
    :return:     Array of points to walk
    """
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
    """
    Solves the Labyrinth

    :param lab: 2D Array which stores the labyrinth to solve
    :param sp:  Starting Point [x,y]
    :param ep:  End Point [x,y]
    :return:    An Array of all paths leading to the end point
    """
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