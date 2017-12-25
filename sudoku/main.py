import random
from collections import defaultdict
from functools import reduce
from itertools import product

import daiquiri
import fire
import numpy as np

logger = daiquiri.getLogger(__name__)


def is_valid(board):
    for line in board:
        unique, count = np.unique(line, return_counts=True)
        if (count[unique != 0] > 1).any():
            return False
    for column in board.T:
        unique, count = np.unique(column, return_counts=True)
        if (count[unique != 0] > 1).any():
            return False
    for i, j in product(range(3), range(3)):
        unique, count = np.unique(board[i * 3: (i + 1) * 3, j * 3: (j + 1) * 3],
                                  return_counts=True)
        if (count[unique != 0] > 1).any():
            return False
    return True


def get_choices(board, pos):
    choices = np.arange(1, 10)
    i, j = pos[0] // 3, pos[1] // 3
    submat = board[3 * i:3 * (i + 1), 3 * j:3 * (j + 1)]
    not_available = reduce(np.union1d,
                           [board[pos[0]], board[:, pos[1]], submat.flat])
    return np.setdiff1d(choices, not_available)


def is_filled(board):
    return (board != 0).all()


def remove_random_element(board, n):
    for i in range(n):
        logger.debug("Remove elem %d / %d", i + 1, n)
        while True:
            pos = random.choice(list(zip(*np.where(board != 0))))
            elem = board[pos]
            logger.debug("Remove %s at pos %s", elem, pos)
            if elem:
                board[pos] = 0
                if is_uniquely_solvable(np.copy(board)):
                    break
                board[pos] = elem


def is_uniquely_solvable(board):
    if is_filled(board):
        return True

    pos = (0, 0)
    while board[pos]:
        pos = next_pos(pos)

    choices = get_choices(board, pos)
    logger.debug("Choose between %s at pos %s", choices, pos)

    if choices.size == 0:
        return False

    solvables = []
    for choice in choices:
        board[pos] = choice
        solvables.append(is_uniquely_solvable(board))
    if sum(solvables) == 1:
        return True
    return False


def create_by_shuffling():
    board1 = np.zeros((9, 9), int)
    board2 = board1.reshape((3, 3, 3, 3))

    for i in range(10):
        logger.info("Create line %d", i)
        random_line = np.arange(1, 10)
        np.random.shuffle(random_line)
        board1[i] = random_line
        while not is_valid(board1):
            logger.debug("Reshuffling")
            np.random.shuffle(random_line)
            board1[i] = random_line
        logger.info(board1)


def next_pos(pos):
    line, col = pos
    if col + 1 > 8:
        return line + 1, 0
    return line, col + 1


def backtrack(board, pos):
    choices = list(range(1, 10))

    logger.debug("\n%s", board)
    logger.debug("At pos %s", pos)
    logger.debug("Choices are %s", choices)

    while True:
        if not choices:
            logger.debug("No more moves")
            return False

        choice = np.random.choice(choices)
        board[pos] = choice
        choices.remove(choice)

        if not is_valid(board):
            logger.debug("Invalid position")
            logger.debug("\n%s", board)
            board[pos] = 0
            continue

        if pos == (8, 8):
            return True

        if not backtrack(board, next_pos(pos)):
            board[pos] = 0
            continue

        return True


def create_by_backtracking():
    board = np.zeros((9, 9), int)
    attempted_numbers = defaultdict(set)
    random_line = np.arange(1, 10)
    np.random.shuffle(random_line)
    board[0] = random_line
    pos = (1, 0)
    backtrack(board, pos)
    return board


def draw_sudoku(board):
    for i in range(9):
        for j in range(9):
            if board[i, j]:
                print(board[i, j], end=" ")
            else:
                print(" ", end=" ")
            if j in (2, 5):
                print("|", end=" ")
        print("\n", end="")
        if i in (2, 5):
            print(20 * "-")


def vectorize(board):
    board.reshape((-1, 9, 9))
    board_vec = np.zeros((*board.shape, 9), int)
    for k in range(board_vec.shape[0]):
        for i in range(board_vec.shape[1]):
            for j in range(board_vec.shape[2]):
                if board[k, i, j]:
                    index = board[k, i, j] - 1
                    board_vec[k, i, j, index] = 1
    return board_vec


def main(n, level="info", out="print"):
    daiquiri.setup(level=getattr(daiquiri.logging, level.upper()))
    solution_board = create_by_backtracking()
    board = np.copy(solution_board)
    remove_random_element(board, n)
    if out == "print":
        draw_sudoku(board)
        print("Lösung:")
        draw_sudoku(solution_board)
    elif out == "vector":
        return vectorize(board), vectorize(solution_board)
    else:
        raise NameError("Unknown value for out")


if __name__ == "__main__":
    fire.Fire()
