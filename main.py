from functools import cache
from typing import Callable


def one_func(x: bool) -> int:
    return 1 if x else 0


def two_func(x: bool) -> int:
    return 2 if x else 0


@cache
def getMatrix(length: int) -> list[list[Callable[[bool], int]]]:
    return [[one_func if ((i < length) == (j < length)) else two_func for i in range(length * 2)] for j in
            range(length * 2)]


def check(top: list[int], left: list[int], board: list[list[bool]], length: int) -> bool:
    board_funcs = getMatrix(length)
    board_int = [[board_funcs[i][j](board[i][j]) for i in range(length * 2)] for j in range(length * 2)]
    row_sum = [sum(row) for row in board_int]
    if row_sum != left:
        return False
    col_sum = [sum(row[i] for row in board_int) for i in range(length * 2)]
    return col_sum == top


def solve(top: list[int], left: list[int],
          board: list[list[bool]], x: int, y: int, length: int) -> bool:
    full_length = length * 2  # total side length
    if y >= full_length:
        return check(top, left, board, length)
    next_x = (x + 1) % full_length
    next_y = y + (1 if x + 1 == full_length else 0)
    board[x][y] = False
    if solve(top, left, board, next_x, next_y, length):
        return True
    board[x][y] = True
    if solve(top, left, board, next_x, next_y, length):
        return True
    return False


def skip(left: list[int], top: list[int], length: int) -> bool:
    for i in range(length-1):  # non-increasing
        if left[i] < left[i+1]:
            return True
        if left[i+length] < left[i+length+1]:
            return True
        if top[i] < top[i+1]:
            return True
        if top[i+length] < top[i+length+1]:
            return True

    if sum(left) != sum(top):  # sum constraint
        return True
    if (sum(left[:length]) % 2) != (sum(top[:length]) % 2):  # parity constraint
        return True
    return False


def gen_constraints(length: int):
    top = [1] * (length * 2)  # non-increasing
    left = [1] * (length * 2)
    length = len(top) // 2
    min_constraint = 1
    max_constraint = 3 * length
    while True:
        if not skip(left, top, length):
            yield top, left
        # gen next
        carry = 1
        for idx in range(length * 2):
            if top[idx] + carry > max_constraint:
                top[idx] = 1
                continue
            else:
                top[idx] += 1
                carry = 0
                break
        if carry == 1:
            for idx in range(length * 2):
                if left[idx] + carry > max_constraint:
                    left[idx] = 1
                    continue
                else:
                    left[idx] += 1
                    carry = 0
                    break
        if carry == 1:
            break


def guess(length):  # length is half the side length of all
    failed = 0
    for left, top in gen_constraints(length):
        board = [[False for _ in range(length * 2)] for _ in range(length * 2)]
        if not solve(top, left, board, 0, 0, length):
            print(top, left)
            failed += 1
    print(f"{failed=}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    guess(2)
