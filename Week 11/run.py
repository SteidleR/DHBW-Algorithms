app_info = {
"Title": "Connect 4",
"ShortSum": "Connect 4: Player vs Computer",
"LongDescr": "Connect 4 Game (Ascii or GUI) with strong Computer Opponent. Minimax-Algorithm used for computer player.",
"Author": "Robin Steidle",
"Version": "0.0",
"LastEdit": "15.06.2020"
}

import random
from tree import Node, printTree

import time

board = [
    [0, 0, 0, 0, 0, 0], # Column
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]

player_ind = {-1: ["X", "red"], 1: ["O", "yellow"]}

# Style: 0 (Ascii Game), 1 (GUI)
style = 0

# strength of computer
level = [["easy", 2], ["medium", 4], ["hard", 6]]

def boardInit():
    """Initialize Board

    Returns:
        list: 2d Array storing board
    """
    return board.copy()

def boardPrint(board: list):
    """Outputs the board on the Terminal or as GUI

    Args:
        board (list): 2D array storing the board
    """
    if style == 0:
        for i in range(6):
            print("| " + " | ".join(str(player_ind[board[j][i]][style] if board[j][i]!=0 else " ") for j in range(7)) + " |")
            print("-"*29)
    else:
        pass


def checkVictoryCol(board: list, player: int, col: int) -> bool:
    count = 0
    for i in range(6):
        if board[col][i] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False


def checkVictoryRow(board: list, player: int, row: int) -> bool:
    count = 0
    for i in range(7):
        if board[i][row] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False


def checkVictoryDia(board: list, player: int) -> bool:
    count = 0
    for i in range(3):
        for j in range(4):
            for p in range(4):
                if board[j+p][i+p] == player: 
                    count += 1
                    if count == 4: return True
                else: count = 0
            count = 0
        count = 0
    
    for i in range(3):
        for j in range(3,7):
            for p in range(4):
                if board[j-p][i+p] == player: 
                    count += 1
                    if count == 4: return True
                else: count = 0
            count = 0
        count = 0
    return False


def checkVictory(board: list, player: int) -> bool:
    """Checks the board for victory

    Args:
        board (list): 2D array storing the board
        player (int): player index (-1 or 1)
    
    Returns:
        bool: is Victory
    """
    for col in range(7):
        if checkVictoryCol(board, player, col):
            return True
    for row in range(6):
        if checkVictoryRow(board, player, row):
            return True
    if checkVictoryDia(board, player):
        return True
    return False


def findOpenRow(board: list, col: int) -> int:
    for i in range(1, 7):
        if board[col][-i] == 0:
            return -i
    return None


def Move(board: list, player: int, col: int) -> bool:
    """Sets the player index in the game array

    Args:
        player (int): Playerindex
        col (int): index of column
        board (list): 2D array storing the board
    Raises
        KeyError: Player set already at coordinates
    """
    i = findOpenRow(board, col)
    if i:
        board[col][i] = player
        return True
    else: 
        return False


def unMove(board: list, col: int):
    """Removes the last move in the given column

    Args:
        board (list): 2d Array storing the board
        col (int): index of column
    """
    i = findOpenRow(board, col)
    if i:
        board[col][i+1] = 0
    else:
        board[col][0] = 0


def boardBasicEval(board: list, player: int, opponent: int) -> int:
    """Calculates a Scalar for the given board

    Args:
        board (list): 2D array storing the board
        player (int): current player
        opponent (int): other player

    Returns:
        int: a scalar that describes the current situation on the board
    """
    if checkVictory(board, player):
        return 1
    elif checkVictory(board, opponent):
        return -1
    else:
        return 0


def createTree(board: int, player: int, opponent: int, func: int, level: int, parent: int):
    """Generates a Minimax-Tree

    Args:
        board (list): 2D array storing the board
        player (int): player index
        opponent (int): opponent index
        level (int): available levels to complete
        parent (class:tree.Node): parent node to add to

    Returns:
        None: to break the function
    """
    for col in range(7):
        if not Move(board, player, col):
            return
        node = Node(0, parent=parent)
        if level > 0:
            createTree(board, -player, -opponent, -func, level-1, node)
            v = node.getChildValues()
            v.sort()
            node.name = v[0 if func<0 else -1]
        else:
            basicEval = boardBasicEval(board, player, opponent)
            node.name = basicEval
        unMove(board, col)


def findBestPath(tree: object, func: int) -> [int, int]:
    """Executes the Minimax algorithm

    Args:
        tree (class:tree.Nodes): root Node of tree
        func (int): min (-1) or max (1) is needed

    Returns:
        int, int: evaluation of the board, column index
    """
    if len(tree.children) == 0:
        return tree.name, 0
    nodes = []
    c = 0
    for n in tree.children:
        val, _ = findBestPath(n, -func)
        nodes.append([c, val])
        c += 1
    nodes.sort(key=lambda x: x[1])
    return nodes[0 if func<0 else -1][1], nodes[0 if func<0 else -1][0]


def findMove(board, player, opponent, level) -> int:
    """Find the best Move with the Minimax-Algorithm

    Args:
        board (list): 2D array storing the board
        player (int): player index
        opponent (int): opponent index
        level (int): levels for iteration

    Returns:
        int: index of the best available move
    """
    tree = Node("Start")
    createTree(board, player, opponent, 1, level-1, tree)
    printTree(tree)
    # val, best = findBestPath(tree, 1)
    v = tree.getChildValues()
    val = dict(zip(v, range(len(v))))
    print(val)
    val = sorted(val.items(), key=lambda x: x[1], reverse=True)
    return val[0]


def runAsAscii(board):
    """Game Loop as Terminal Application

    Args:
        board (list): 2D Array storing the board
    """
    player = random.choice([-1, 1])
    u_level = 1
    print("You are Player "+player_ind[player][0])
    boardPrint(board)
    while True:
        try:
            col = int(input("Column to choose (0-6):"))
        except ValueError:
            input("Please type only integer between 0 and 6 [ENTER]")
            continue
        Move(board, player, col)
        boardPrint(board)
        if checkVictory(board, player):
            print("You won the game!")
            break
        bot_move = findMove(board.copy(), -player, player, level[u_level][1])
        Move(board, -player, bot_move)
        boardPrint(board)
        if checkVictory(board, -player):
            print("You lose the game!")
            break
        time.sleep(1)


if __name__ == "__main__":
    print(checkVictory(board, -1))
    r_board = boardInit()
    if style==0:
        runAsAscii(r_board)