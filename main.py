from functools import reduce
from itertools import product
from collections import defaultdict

import numpy as np
import fire
import daiquiri


logger = daiquiri.getLogger(__name__)


def create_random():
    game = np.zeros((9, 9), int)
    for i in range(9):
        game[i] = range(1, 10)
        np.random.shuffle(game[i])
    return game


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
    not_available = reduce(np.union1d, [board[pos[0]], board[:, pos[1]], submat.flat])
    return np.setdiff1d(choices, not_available)


def is_uniquely_solvable(initial_board, pos):
    board = np.copy(initial_board)
    pos = 0, 0
    while board[pos]:
        pos = next_pos(pos)


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


def create_advanced():
    board1 = np.zeros((9, 9), int)
    board2 = board1.reshape((3, 3, 3, 3))

    logger.info("Create line %d", 0)
    random_line = np.arange(1, 10)
    np.random.shuffle(random_line)
    board1[0] = random_line
    for line in range(1, 9):
        for num in range(1, 10):
            for col in range(9):
                if not board1[line, col]:
                    board1[line, col] = num
                    if is_valid(board1):
                        break
                    else:
                        board1[line, col] = 0

        logger.info(board1)


def next_pos(pos):
    line, col = pos
    if col + 1 > 8:
        return line + 1, 0
    return line, col + 1


def backtrack(board, pos):
    choices = list(range(1, 10))

    logger.info("\n%s", board)
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


def main(level="info"):
    daiquiri.setup(level=getattr(daiquiri.logging, level.upper()))
    board = create_by_backtracking()
    print(board)
    print("remove", board[2, 4])
    print("remove", board[2, 5])
    board[2, 4] = 0
    board[2, 5] = 0
    print(get_choices(board, (2, 4)))


if __name__ == "__main__":
    fire.Fire()
