import math
import random
import sys

import numpy as np
import pygame
from pygame.draw import circle

# Constants
ROW_COUNT = 6
COL_COUNT = 7

SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - SQUARESIZE / 20)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)

ELEM_ID = [1, 2]

COLOR_PLAYER = [(255, 0, 0), (255, 255, 0)]

PLAYER = random.choice(ELEM_ID)
BOT = ELEM_ID[-PLAYER]

PLAYER_TURN = PLAYER - 1
BOT_TURN = BOT - 1

EMPTY = 0

WINNING_LEN = 4

SCORE_WIN = 100
SCORE_THREE = 5
SCORE_TWO = 2

SCORE_OPP_THREE = -8


def Move(board, col, row, player):
    board[row][col] = player


def UnMove(board, col):
    row = FindOpenRow(board, col)
    if row is False:
        row = -1
    else:
        row -= 1
    Move(board, col, row, EMPTY)


def BoardInit():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board


def BoardPrint(board):
    print(np.flip(board, 0))


def BoardDraw(board, screen, height):
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (col * SQUARESIZE, row * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            circle(screen, BLACK,  (int(SQUARESIZE * (0.5 + col)), int(SQUARESIZE * (1.5 + row))), RADIUS)
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT):
            index = int(board[row][col])
            if index != 0:
                circle(screen, COLOR_PLAYER[index - 1],
                       (int(SQUARESIZE * (0.5 + col)), height - int(SQUARESIZE * (0.5 + row))), int(RADIUS * 0.95))
    pygame.display.update()


def FindOpenRow(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row
    return False


def CheckVictoryHorizontal(board, player):
    for col in range(COL_COUNT - 3):
        for row in range(ROW_COUNT):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] == player:
                return True


def CheckVictoryVertical(board, player):
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT - 3):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] == player:
                return True


def CheckVictoryDiagonalPos(board, player):
    for col in range(COL_COUNT - 3):
        for row in range(ROW_COUNT - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] \
                    == board[row + 3][col + 3] == player:
                return True


def CheckVictoryDiagonalNeg(board, player):
    for col in range(COL_COUNT - 3):
        for row in range(3, ROW_COUNT):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] \
                    == board[row - 3][col + 3] == player:
                return True


def CheckVictory(board, player):
    return CheckVictoryHorizontal(board, player) or CheckVictoryVertical(board, player) \
           or CheckVictoryDiagonalPos(board, player) or CheckVictoryDiagonalNeg(board, player)


def EvalWindow(window, player):
    opponent = 1 - player

    score = 0
    if window.count(player) == 4:
        score += SCORE_WIN
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += SCORE_THREE
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += SCORE_TWO

    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score += SCORE_OPP_THREE

    return score


def IsTerminalNode(board):
    return CheckVictory(board, PLAYER) or CheckVictory(board, BOT) or len(GetAvailableMoves(board)) == 0


def GetAvailableMoves(board):
    moves = []
    for col in range(COL_COUNT):
        if type(FindOpenRow(board, col)) == int:
            moves.append(col)
    return moves


def BoardBasicEval(board, player):
    if CheckVictory(board, player):
        return 1
    elif CheckVictory(board, 1 - player):
        return -1
    else:
        return 0


def BoardBetterEval(board, player):
    score = 0

    # Center Column
    center_array = [int(i) for i in list(board[:, COL_COUNT // 2])]
    center_count = center_array.count(player)
    score += center_count * 3

    # Horizontal Score
    for row in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[row, :])]
        for col in range(COL_COUNT - 3):
            window = row_array[col:col + WINNING_LEN]
            score += EvalWindow(window, player)

    # Vertical Score
    for col in range(COL_COUNT):
        col_array = [int(i) for i in list(board[:, col])]
        for row in range(ROW_COUNT - 3):
            window = col_array[row:row + WINNING_LEN]
            score += EvalWindow(window, player)

    # Positive Diagonal Score
    for row in range(ROW_COUNT - 3):
        for col in range(COL_COUNT - 3):
            window = [board[row + i][col + i] for i in range(WINNING_LEN)]
            score += EvalWindow(window, player)

    # Negative Diagonal Score
    for row in range(ROW_COUNT - 3):
        for col in range(COL_COUNT - 3):
            window = [board[row + 3 - i][col + i] for i in range(WINNING_LEN)]
            score += EvalWindow(window, player)

    return score


def minimax(board, depth, alpha, beta, maximizing_player):
    valid_moves = GetAvailableMoves(board)
    if depth == 0 or IsTerminalNode(board):
        if depth != 0:
            if CheckVictory(board, BOT):
                return None, 10000000
            elif CheckVictory(board, PLAYER):
                return None, -10000000
            else:
                return None, 0
        else:
            return None, BoardBetterEval(board, BOT)

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_moves)
        for col in valid_moves:
            row = FindOpenRow(board, col)
            Move(board, col, row, BOT)
            _, new_score = minimax(board, depth - 1, alpha, beta, False)
            UnMove(board, col)
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        value = math.inf
        column = random.choice(valid_moves)
        for col in valid_moves:
            row = FindOpenRow(board, col)
            Move(board, col, row, PLAYER)
            _, new_score = minimax(board, depth - 1, alpha, beta, True)
            UnMove(board, col)
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def FindMove(board, player):
    valid_moves = GetAvailableMoves(board)
    best = -10000
    best_col = random.choice(valid_moves)
    for col in valid_moves:
        row = FindOpenRow(board, col)
        Move(board, col, row, player)
        score = BoardBasicEval(board, player)
        UnMove(board, col)
        if score > best:
            best = score
            best_col = col

    return best_col


class Bot:
    def __init__(self, player=2, level=0):
        if level == 0:
            self.method = "Basic"
        else:
            self.method = "Advanced"
        self.levels = {1: ["easy", 2], 2: ["intermediate", 3], 3: ["Hard", 4], 4: ["Impossible", 6]}
        self.depth = self.levels[level][1]
        self.player = player

    def Move(self, board):
        row = False
        col = None
        if self.method == "Basic":
            while type(row) != int:
                col = FindMove(board, self.player)
                row = FindOpenRow(board, col)
        else:
            while type(row) != int:
                col, score = minimax(board, self.depth, -math.inf, math.inf, True)
                row = FindOpenRow(board, col)
        Move(board, col, row, ELEM_ID[self.player])


def Game():
    board = BoardInit()
    game_over = False
    turn = 0

    non_player = False

    bot = Bot(BOT_TURN, level=4)

    bot2 = None
    if "non-player" in sys.argv:
        non_player = True
        bot2 = Bot(PLAYER_TURN, level=4)

    pygame.init()
    width = COL_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect 4")
    while not game_over:
        BoardDraw(board, screen, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                if turn == PLAYER_TURN:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    circle(screen, COLOR_PLAYER[turn], (event.pos[0], int(SQUARESIZE / 2)), int(RADIUS * 0.9))

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == PLAYER_TURN and not non_player:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
                    row = FindOpenRow(board, col)
                    if type(row) == int:
                        Move(board, col, row, ELEM_ID[turn])
                        if CheckVictory(board, ELEM_ID[turn]):
                            print("Player Wins!")
                            game_over = True
                        turn += 1
                        turn = turn % 2

        if non_player:
            if turn == PLAYER_TURN and not game_over:
                # col = FindMove(board, BOT)
                bot2.Move(board)
                if CheckVictory(board, ELEM_ID[turn]):
                    print("Bot 2 Wins!")
                    game_over = True
                turn += 1
                turn = turn % 2

        if turn == BOT_TURN and not game_over:
            # col = FindMove(board, BOT)
            bot.Move(board)
            if CheckVictory(board, ELEM_ID[turn]):
                print("Bot Wins!")
                game_over = True
            turn += 1
            turn = turn % 2

    BoardDraw(board, screen, height)


if __name__ == "__main__":
    Game()
