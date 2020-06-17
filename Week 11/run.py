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

def boardPrint(board):
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

def checkVictoryCol(board, player, col):
    """Check Victory in given Column for player index

    Args:
        board (list): 2D array
        player (int): player index (-1 or 1)
        col (int): Column index (range: 0-6)

    Returns:
        bool: is Victory
    """
    count = 0
    for i in range(6):
        if board[col][i] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def checkVictoryRow(board, player, row):
    """Check Victory in given Row for player index

    Args:
        board (list): 2D array
        player (int): player index (-1 or 1)
        row (int): Row index (range: 0-6)

    Returns:
        bool: is Victory
    """
    count = 0
    for i in range(7):
        if board[i][row] == player:
            count += 1
            if count == 4:
                return True
        else:
            count = 0
    return False

def checkVictoryDia(board, player):
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

def checkVictory(board, player):
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
    

def findOpenRow(board, col):
    """Search a column for the lowest open row

    Args:
        board (list): 2D array storing the board
        col (int): index of column in list

    Returns:
        int: index of lowest open row
    """
    for i in range(1, 7):
        if board[col][-i] == 0:
            return -i
    return None

def Move(board, player, col):
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

def unMove(board, col):
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

def countCol(board, player, n):
    """

    Args:
        board (list): 2D array storing the board
        player (int): player index
        n (int): count of consecutive player elements

    Returns:
        int: generated points
    """
    points = 0
    for col in range(7):
        count = 0
        for i in range(6):
            if board[col][i] == player:
                count += 1
                if count == n:
                    points += 2**n
                    count = 0
            else:
                count = 0
    return points

def countRow(board, player, n):
    points = 0
    for row in range(6):
        count = 0
        for i in range(7):
            if board[i][row] == player:
                count += 1
                if count == n:
                    points += 2**n
                    count = 0
            else:
                count = 0
    return points

def countDiagonal(board, player, n):
    count = 0
    points = 0
    for i in range(3):
        for j in range(4):
            for p in range(4):
                if board[j+p][i+p] == player: 
                    count += 1
                    if count == n: 
                        points += 2**n
                        count = 0
                else: 
                    count = 0
            count = 0
        count = 0
    
    for i in range(3):
        for j in range(3,7):
            for p in range(4):
                if board[j-p][i+p] == player: 
                    count += 1
                    if count == 4: 
                        points += 2**n
                        count = 0
                else: 
                    count = 0
            count = 0
        count = 0
    return points

def boardBasicEval(board, player, opponent):
    """Calculates a Scalar for the given board

    Args:
        board (list): 2D array storing the board
        player (int): current player
        opponent (int): other player

    Returns:
        int: a scalar that describes the current situation on the board
    """
    points = 0

    if checkVictory(board, player):
        return 500
    for i in range(2,4):
        points += countCol(board, player, i)
        points += countRow(board, player, i)
        points += countDiagonal(board, player, i)

    if checkVictory(board, -player):
        return 500
    for i in range(2,4):
        points -= countCol(board, opponent, i)
        points -= countRow(board, opponent, i)
        points -= countDiagonal(board, opponent, i)  
    return points

def createTree(board, player, opponent, level, parent):
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
    tree = []
    for col in range(7):
        if not Move(board, player, col):
            return
        basicEval = boardBasicEval(board, player, opponent)
        node = Node(basicEval, parent=parent)
        if level > 0:
            createTree(board, -player, -opponent, level-1, node)
        unMove(board, col)

def findBestPath(tree, func) -> int,int:
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
    createTree(board, player, opponent, level-1, tree)
    val, best = findBestPath(tree, 1)
    printTree(tree)
    print(best, val)
    return best


def runAsAscii(board):
    """Game Loop as Terminal Application

    Args:
        board (list): 2D Array storing the board
    """
    player = random.choice([-1, 1])
    u_level = 0
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

if __name__ == "__main__":
    print(checkVictory(board, -1))
    r_board = boardInit()
    if style==0:
        runAsAscii(r_board)