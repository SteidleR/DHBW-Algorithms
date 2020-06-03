import sys
sys.setrecursionlimit(10**5) 

labname = "lab.txt"
step = {"U": [0, -1], "D": [0, 1], "R": [1, 0], "L": [-1, 0]}

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


# ----------- Functions to solve the Lab ----------------


def checkNeighbors(x, y, px, py, lab):
    nextp = []

    for key, val in step.items():
        if px-val[0] == x and py-val[1] == y:
            continue
        if lab[y+val[1]][x+val[0]] != "#":
            nextp.append(key)
    return nextp

def walk(x, y, px, py, lab):
    path = {}
    if x == ex and y == ey:
        return True
    steps = checkNeighbors(x, y, px, py, lab)
    if steps == []:
        return False
    for w in steps:
        path[w] = walk(x+step[w][0], y+step[w][1], x, y, lab)
    return path

def solveLab(lab):
    tree = {"S": walk(sx, sy, sx, sy, lab)}
    def loop(path):
        paths = []
        for key, val in path.items():
            if val == True:
                paths.append("X")
            else:
                p = loop(val)
                for x in p:
                    paths.append(key+x)
        return paths
    return(loop(tree))


# ----------------------------------------------------------

if __name__ == "__main__": 

    print(solveLab(readLab(labname)))