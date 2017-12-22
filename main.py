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
    b2 = board.reshape((3, 3, 3, 3))
    for line in board:
        unique, count = np.unique(line, return_counts=True)
        if (count[unique != 0] > 1).any():
            return False
    for column in board.T:
        unique, count = np.unique(column, return_counts=True)
        if (count[unique != 0] > 1).any():
            return False
    for i, j in product(range(b2.shape[0]), range(b2.shape[1])):
        unique, count = np.unique(b2[i, j], return_counts=True)
        if (count[unique != 0] > 1).any():
            return False
    return True


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


def backtr(board, attempts, pos):
    digits = set(range(1, 10))
    choices = list(digits - attempts[pos])

    logger.debug(board)
    logger.debug("At pos %s", pos)
    logger.debug("Choices are %s", choices)

    while True:
        if not choices:
            logger.debug("No more moves")
            return False

        choice = np.random.choice(choices)
        board[pos] = choice
        attempts[pos].add(choice)
        choices.remove(choice)

        if not is_valid(board):
            logger.debug("Invalid position")
            board[pos] = 0
            continue

        if not backtr(board, attempts, next_pos(pos)):
            board[pos] = 0
            continue


def backtrack():
    board1 = np.zeros((9, 9), int)
    attempted_numbers = defaultdict(set)
    random_line = np.arange(1, 10)
    np.random.shuffle(random_line)
    board1[0] = random_line
    pos = (1, 0)
    attempts = defaultdict(set)
    backtr(board1, attempts, pos)
    print(board1)
    print(is_valid(board1))
    print(attempts)


def main(level="info"):
    daiquiri.setup(level=getattr(daiquiri.logging, level.upper()))
    backtrack()


if __name__ == "__main__":
    fire.Fire()
    main()
