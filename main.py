def check(top_one: list[int], top_two: list[int], left_one: list[int], left_two: list[int], board: list[list[bool]]) -> bool:
    return True # TODO: implement check


def solve(top_one: list[int], top_two: list[int], left_one: list[int], left_two: list[int],
          board: list[list[bool]], x: int, y: int):
    length = len(top_one) * 2 # total side length
    if x >= length:
        return check(top_one, top_two, left_one, left_two, board)
    next_x = (x + 1) % length
    next_y = y + (1 if x + 1 == length else 0)
    board[x][y] = False
    solve(top_one, top_two, left_one, left_two, board, next_x, next_y)
    board[x][y] = True
    solve(top_one, top_two, left_one, left_two, board, next_x, next_y)



def inc(top_one: list[int], top_two: list[int], left_one: list[int], left_two: list[int]):
    length = len(top_one)
    minConstraint = 1
    maxConstraint = 3*length
    pass #TODO: implement inc

def guess(length): # length is half the side length of all
    top_one = [1] * length # non-increasing
    top_two = [1] * length
    left_one = [1] * length
    left_two  = [1] * length
    def skip() -> bool:
        if sum(left_one) + sum(left_two) != sum(top_one) + sum(top_two):
            return True
        if sum(left_one) % 2 != sum(top_one) % 2:
            return True
        return False
    incorrect = 0
    while True:
        if not skip():
            board = [[False for _ in range(length * 2)] for _ in range(length * 2)]
            solve(top_one, top_two, left_one, left_two, board, 0, 0)
        if inc(top_one, top_two, left_two, left_two):
            break
    print("Total incorrect: ", incorrect)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    guess(2)


