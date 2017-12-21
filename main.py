from itertools import product

import numpy as np


def create_random():
    game = np.zeros((9, 9), int)
    for i in range(9):
        game[i] = range(1, 10)
        np.random.shuffle(game[i])
    return game


def check_partial(board):
    pass


def is_valid(board):
    b2 = board.reshape((3, 3, 3, 3))
    for line in board:
        if not np.in1d(range(1, 10), line).all():
            return False
    for column in board.T:
        if not np.in1d(range(1, 10), column).all():
            return False
    for i, j in product(range(b2.shape[0]), range(b2.shape[1])):
        if not np.in1d(range(1, 10), b2[i, j]):
            return False
    return True


def create():
    board1 = np.zeros((9, 9), int)
    board2 = board1.reshape((3, 3, 3, 3))
