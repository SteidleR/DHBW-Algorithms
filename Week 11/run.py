import numpy as np
import pygame
import sys
import math

# Constants
ROW_COUNT = 6
COL_COUNT = 7

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - SQUARESIZE/20)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER = [1, 2]
COLOR_PLAYER = [RED, YELLOW]


def BoardInit():
    board = np.zeros((ROW_COUNT, COL_COUNT))
    return board


def BoardPrint(board):
    print(np.flip(board, 0))


def BoardDraw(board):
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK,
                               (int(col * SQUARESIZE + SQUARESIZE / 2), int(row * SQUARESIZE + SQUARESIZE * 1.5)),
                               RADIUS)
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT):
            index = int(board[row][col])
            if index != 0:
                pygame.draw.circle(screen, COLOR_PLAYER[index-1],
                                   (int(col * SQUARESIZE + SQUARESIZE / 2), height-int(row * SQUARESIZE + SQUARESIZE * 0.5)),
                                   int(RADIUS * 0.95))

    pygame.display.update()


def FindOpenRow(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row
    return False


def CheckVictory(board, player):
    # Horizontal Win
    for col in range(COL_COUNT-3):
        for row in range(ROW_COUNT):
            if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] == player:
                return True

    # Vertical Win
    for col in range(COL_COUNT):
        for row in range(ROW_COUNT-3):
            if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] == player:
                return True

    # Check positive diagonal Win
    for col in range(COL_COUNT-3):
        for row in range(ROW_COUNT-3):
            if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] == player:
                return True

    # Check negative diagonal Win
    for col in range(COL_COUNT-3):
        for row in range(3, ROW_COUNT):
            if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] == player:
                return True


def Move(board, col, row, player):
    board[row][col] = player


if __name__ == "__main__":

    board = BoardInit()
    game_over = False
    turn = 0

    pygame.init()
    width = COL_COUNT * SQUARESIZE
    height = (ROW_COUNT+1) * SQUARESIZE
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Connect 4")
    BoardDraw(board)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                pygame.draw.circle(screen, COLOR_PLAYER[turn], (posx, int(SQUARESIZE/2)), int(RADIUS*0.9))
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
                    row = FindOpenRow(board, col)
                    if type(row) == int:
                        Move(board, col, row, PLAYER[turn])
                        if CheckVictory(board, PLAYER[turn]):
                            print("Player 1 Wins!")
                            game_over = True
                        turn += 1
                        turn = turn % 2

                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
                    row = FindOpenRow(board, col)
                    if type(row) == int:
                        Move(board, col, row, PLAYER[turn])
                        if CheckVictory(board, PLAYER[turn]):
                            print("Player 2 Wins!")
                            game_over = True
                        turn += 1
                        turn = turn % 2

                BoardDraw(board)
                
                if game_over:
                    pygame.time.wait(3000)


        """if turn == 0:
            col = int(input("Player 1, Make your turn (0-6): "))
            row = FindOpenRow(board, col)
            if type(row) == int:
                Move(board, col, row, PLAYER[0])

                if CheckVictory(board, PLAYER[0]):
                    print("Player 1 Wins!")
                    game_over = True

        else:
            col = int(input("Player 2, Make your turn (0-6): "))
            row = FindOpenRow(board, col)
            if type(row) == int:
                Move(board, col, row, PLAYER[1])

                if CheckVictory(board, PLAYER[1]):
                    print("Player 2 Wins!")
                    game_over = True

        BoardPrint(board)"""


