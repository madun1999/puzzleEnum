from functools import cache
from itertools import combinations
from typing import Callable
import cProfile

print_sol = False

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
    board_int = [[board_funcs[i][j](board[i][j]) for j in range(length * 2)] for i in range(length * 2)]
    row_sum = [sum(row) for row in board_int]
    if row_sum != left:
        return False
    col_sum = [sum(row[i] for row in board_int) for i in range(length * 2)]
    if col_sum == top:
        if print_sol:
            print(board)
        return True
    return False

def check_row(left: list[int], board: list[list[bool]], length: int, row: int) -> bool:
    board_funcs = getMatrix(length)
    row_int = [board_funcs[row][j](board[row][j]) for j in range(length * 2)]
    row_sum = sum(row_int)
    return row_sum == left[row]

def check_col(top: list[int], board: list[list[bool]], length: int, col: int) -> bool:
    board_funcs = getMatrix(length)
    col_int = [board_funcs[i][col](board[i][col]) for i in range(length * 2)]
    col_sum = sum(col_int)
    return col_sum == top[col]

def solve(top: list[int], left: list[int],
          board: list[list[bool]], x: int, y: int, length: int) -> bool:
    full_length = length * 2  # total side length
    if y >= full_length:
        return check(top, left, board, length)
    next_x = (x + 1) % full_length
    next_y = y + (1 if x + 1 == full_length else 0)

    board[y][x] = False
    if x < full_length - 1 or check_row(left, board, length, y):
        if y < full_length - 1 or check_col(top, board, length, x):
            if solve(top, left, board, next_x, next_y, length):
                return True
    board[y][x] = True
    if x < full_length - 1 or check_row(left, board, length, y):
        if y < full_length - 1 or check_col(top, board, length, x):
            if solve(top, left, board, next_x, next_y, length):
                return True
    return False


def skip(left: list[int], top: list[int], length: int) -> bool:
    # for i in range(length-1):  # skip if not non-increasing 
    #     if left[i] > left[i+1]:
    #         return True
    #     if left[i+length] < left[i+length+1]:
    #         return True
    #     if top[i] < top[i+1]:
    #         return True
    #     if top[i+length] < top[i+length+1]:
    #         return True
    if left == top: # skip if symmetric
        return True
    # if sum(left) != sum(top):  # skip if not sum constraint
    #     return True
    # if (sum(left[:length]) % 2) != (sum(top[:length]) % 2):  # skip if not parity constraint
    #     return True
    
    all_nums = list(set(left + top)) # skip if not almost regular
    if len(set(left + top)) > 2 or (all_nums[0] != all_nums[1] + 1 and all_nums[1] != all_nums[0] + 1):  
        return True
               
    return False


# Modified AccelAsc
# Generating All Partitions: A Comaprison of Two Encodings
# Secion 4.1.2
# Kelleher, Jerome; O'Sullivan, Barry
# prerequisite: length >= 2
def partitions(sumi, length, arr, start):
    for i in range(length): # clear array
        arr[i+start] = 0
    k = 1 # index
    y = sumi - 1 # remaining sum
    while k != 0:
        k -= 1
        x = arr[k + start] + 1 
        while 2 * x <= y and k <= length - 3:
            arr[k + start] = x
            y -= x
            k += 1
        l = k + 1
        while x <= y:
            arr[k + start] = x
            arr[l + start] = y
            yield None
            x += 1
            y -= 1
        y += x - 1
        arr[k + start] = y + 1
        arr[l + start] = 0
        yield None


def gen_constraints(length: int):
    min_constraint = 0
    max_constraint = length * 3
    top = [min_constraint] * (length * 2) 
    left = [min_constraint] * (length * 2)
    min_sector_sum = min_constraint * length
    max_sector_sum = max_constraint * length 
    top_sectors = [0] * 2
    left_sectors = [0] * 2
    while True:
        for left_sector_zero_sum in range(top_sectors[0] % 2, sum(top_sectors) + 1, 2):
            left_sectors[0] = left_sector_zero_sum
            left_sectors[1] = sum(top_sectors) - left_sector_zero_sum
            for _ in partitions(top_sectors[0], length, top, 0):
                for _ in partitions(top_sectors[1], length, top, length):
                    for _ in partitions(left_sectors[0], length, left, 0):
                        for _ in partitions(left_sectors[1], length, left, length):
                            if not skip(left, top, length):   
                                yield left, top
        # gen next top_sectors
        carry = 1
        # add one to top
        for idx in range(2):
            if top_sectors[idx] + carry > max_sector_sum:
                top_sectors[idx] = min_sector_sum
                continue
            else:
                top_sectors[idx] += 1
                carry = 0
                break
        if carry == 1:
            break



def guess(length):  # length is half the side length of all
    failed = 0
    good = 0
    for left, top in gen_constraints(length):
        board = [[False for _ in range(length * 2)] for _ in range(length * 2)]
        if solve(top, left, board, 0, 0, length):
            print("Good:", top, left)
            good += 1
        else: 
            print("Failed:", top, left)
            failed += 1
    print(f"{failed=} {good=}")


if __name__ == '__main__':

    print_sol = False

    # length = 2
    # board = [[False for _ in range(length * 2)] for _ in range(length * 2)]
    # board = [[True, False, False, False], [False, True, False, False], [True, False, True, False], [False, False, False, True]]
    # print(solve([2,2,1,1],[1,1,2,2], board, 0, 0, length))
    guess(3)
    # cProfile.run('guess(3)')
    # print(sorted([(1,2),(2,1)]))
    
