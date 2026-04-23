import pyxel
import random

CELL_SIZE = 20
GRID_SIZE = 9
WIDTH = CELL_SIZE * GRID_SIZE
HEIGHT = CELL_SIZE * GRID_SIZE

import random

SIZE = 9

def is_valid(board, row, col, num):
    # 行
    if num in board[row]:
        return False
    
    # 列
    if num in [board[r][col] for r in range(SIZE)]:
        return False
    
    # 3x3ブロック
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True


def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if fill_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True


def generate_complete_board():
    board = [[0] * SIZE for _ in range(SIZE)]
    fill_board(board)
    return board

def count_solutions(board):
    count = 0

    def solve():
        nonlocal count
        if count > 1:
            return
        
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            solve()
                            board[row][col] = 0
                    return
        count += 1

    solve()
    return count

def generate_puzzle(board, attempts=40):
    puzzle = [row[:] for row in board]

    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        if puzzle[row][col] == 0:
            continue

        backup = puzzle[row][col]
        puzzle[row][col] = 0

        # 解が一意かチェック
        board_copy = [r[:] for r in puzzle]
        if count_solutions(board_copy) != 1:
            puzzle[row][col] = backup
            attempts -= 1

    return puzzle

class SudokuApp:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Sudoku")

        complete = generate_complete_board()
        self.board = generate_puzzle(complete)

        self.fixed = [[cell != 0 for cell in row] for row in self.board]

        # 0 = 空
#        self.board = [[0]*9 for _ in range(9)]

        # 固定マス（問題）
#        self.fixed = [[False]*9 for _ in range(9)]

        # カーソル
        self.cursor_x = 0
        self.cursor_y = 0

        pyxel.run(self.update, self.draw)

    def update(self):
        # カーソル移動
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.cursor_x = (self.cursor_x - 1) % 9
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.cursor_x = (self.cursor_x + 1) % 9
        if pyxel.btnp(pyxel.KEY_UP):
            self.cursor_y = (self.cursor_y - 1) % 9
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.cursor_y = (self.cursor_y + 1) % 9

        # 数字入力（1〜9）
        for i in range(1, 10):
            if pyxel.btnp(getattr(pyxel, f"KEY_{i}")):
                if not self.fixed[self.cursor_y][self.cursor_x]:
                    self.board[self.cursor_y][self.cursor_x] = i

        # 消す（0 or BACKSPACE）
        if pyxel.btnp(pyxel.KEY_BACKSPACE) or pyxel.btnp(pyxel.KEY_0):
            if not self.fixed[self.cursor_y][self.cursor_x]:
                self.board[self.cursor_y][self.cursor_x] = 0

    def draw(self):
        pyxel.cls(0)

        # グリッド描画
        for y in range(9):
            for x in range(9):
                px = x * CELL_SIZE
                py = y * CELL_SIZE

                # カーソルハイライト
                if x == self.cursor_x and y == self.cursor_y:
                    pyxel.rect(px, py, CELL_SIZE, CELL_SIZE, 1)

                # 数字
                val = self.board[y][x]
                if val != 0:
                    color = 7 if self.fixed[y][x] else 10
                    pyxel.text(px+6, py+6, str(val), color)

        # 太線（3x3区切り）
        for i in range(10):
            thickness = 2 if i % 3 == 0 else 1
            pyxel.line(0, i*CELL_SIZE, WIDTH, i*CELL_SIZE, 7)
            pyxel.line(i*CELL_SIZE, 0, i*CELL_SIZE, HEIGHT, 7)


SudokuApp()