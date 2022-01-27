import time
import tkinter as tk
from tkinter import messagebox
from copy import deepcopy

from data import CLEAN_BOARD, EASY_BOARD, MEDIUM_BOARD, HARD_BOARD

PREBUILT_BOARDS = {
    'clean': CLEAN_BOARD,
    'easy': EASY_BOARD,
    'medium': MEDIUM_BOARD,
    'hard': HARD_BOARD
}


class Solver(object):
    """class for the sudoku board solver"""

    def __init__(self):
        self.board = deepcopy(PREBUILT_BOARDS['medium'])
        self.algorithms = {
            'backtracking': self.backtracking,
            'csp_backtracking': self.csp_backtracking,
        }

    def __str__(self, time, mode):
        """prints the solved sudoku board with 3x3 separators"""
        string = ""
        for i in range(9):
            if i % 3 == 0:
                string += "-------------------------\n"
            for j in range(9):
                if j % 3 == 0:
                    string += "| "
                string += str(self.board[i][j]) + " "
            string += "|\n"
        string += "-------------------------"
        return string

    def update_board(self, tkapp: tk.Tk = None, board: str = None):
        """initializes the sudoku board"""
        if board is not None:
            tmp = deepcopy(PREBUILT_BOARDS[board])
        else:
            tmp = self.board

        # update the board in the GUI
        for i in range(9):
            for j in range(9):
                txt_input = ''
                if tmp[i][j] != '0':
                    txt_input = tmp[i][j]
                tkapp.board_cells[i][j].config(
                    text=tk.StringVar(value=txt_input))
                self.board[i][j] = tmp[i][j]

    def getNextLocation(self):
        """get next empty cell on the board"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == '0':
                    return (i, j)
        return (-1, -1)

    def isValid(self, row: int, col: int, num: int):
        """checks if the number is valid in the row, column and 3x3 square"""
        if not num.isdigit():
            return False
        if int(num) < 1 or int(num) > 9:
            return False
        if num in self.board[row]:
            return False
        if num in tuple(zip(*self.board))[col]:
            return False
        start_row, start_col = row // 3 * 3, col // 3 * 3
        if any([num in x for x in tuple(zip(*self.board[start_row: start_row + 3]))[start_col: start_col + 3]]):
            return False
        return True

    def getDomain(self):
        """get all the possible remaining values for each cell"""
        domain = []
        for row in range(len(self.board)):
            col_domain = []
            for col in range(len(self.board[0])):
                if self.board[row][col] != '0':
                    col_domain.append(['x'])
                else:
                    RVCell = [str(i) for i in range(1, len(self.board) + 1)]
                    for i in range(len(self.board)):
                        if self.board[row][i] != '0':
                            if self.board[row][i] in RVCell:
                                RVCell.remove(self.board[row][i])

                    for i in range(len(self.board)):
                        if self.board[i][col] != '0':
                            if self.board[i][col] in RVCell:
                                RVCell.remove(self.board[i][col])

                    boxRow = row - row % 3
                    boxCol = col - col % 3
                    for i in range(3):
                        for j in range(3):
                            if self.board[boxRow+i][boxCol+j] != 0:
                                if self.board[boxRow+i][boxCol+j] in RVCell:
                                    RVCell.remove(
                                        self.board[boxRow+i][boxCol+j])
                    col_domain.append(RVCell)
            domain.append(col_domain)
        return domain

    def isEmptyDomainProduced(self, row, col):
        """check if any domain will be empty after the current assignment"""
        element = self.rv[row].pop(col)
        for i in range(len(self.rv)):
            if [] in self.rv[i]:
                self.rv[row].insert(col, element)
                return True
        else:
            self.rv[row].insert(col, element)
            return False

    def csp_backtracking(self):
        """solves the sudoku board using CSP backtracking algorithm."""
        location = self.getNextLocation()

        if location == (-1, -1):
            return True
        else:
            self.iteration += 1
            i, j = location
            for choice in self.rv[i][j]:
                self.board[i][j] = choice
                cpy = deepcopy(self.rv)
                self.rv = self.getDomain()
                if not self.isEmptyDomainProduced(i, j):
                    if self.csp_backtracking():
                        return True
                self.board[i][j] = '0'
                self.rv = cpy
            return False

    def backtracking(self):
        """solves the sudoku board using backtracking algorithm."""
        location = self.getNextLocation()

        if location == (-1, -1):
            return True
        else:
            self.iteration += 1
            i, j = location
            for n in range(1, 10):
                if self.isValid(i, j, str(n)):
                    self.board[i][j] = str(n)
                    if self.backtracking():
                        return True
                    self.board[i][j] = '0'
            return False

    def solve(self, tkapp: tk.Tk = None, method: str = 'csp_backtracking'):
        """solves the sudoku board with a given method"""
        if method not in self.algorithms:
            # raise ValueError('Invalid method')
            messagebox.showwarning(
                title=None,
                message='Please choose a valid algorithm.',
            )
            return

        self.iteration = 0
        for i in range(9):
            for j in range(9):
                cell_val = tkapp.board_cells[i][j].get()
                if cell_val == '':
                    cell_val = '0'
                self.board[i][j] = cell_val

        if method == 'csp_backtracking':
            self.rv = self.getDomain()

        start = time.time()
        self.algorithms[method]()
        elapsed = time.time() - start
        # check if there's any 0 on the board
        if any(['0' in row for row in self.board]):
            messagebox.showerror(
                title=None,
                message='No solution found.',
            )
            return
        else:
            txt_info = (
                f'iterations: {self.iteration} time taken: {elapsed:.3f}s'
            )
            messagebox.showinfo(
                title=method,
                message=txt_info
            )
            self.update_board(tkapp)


class SudokuApp(tk.Tk):
    """class to create the sudoku tkinter app"""

    def __init__(self, sudoku):
        super().__init__()
        self.sudoku = sudoku
        self.title('Sudoku Solver')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        """creates the widgets for the tkinter app"""

        # create the sudoku board table
        self.table = tk.Frame(self, bg='#f0f0f0')
        self.table.grid(row=0, column=0, sticky='nsew',
                        pady=10, padx=10)

        # fill the sudoku board
        self.board_cells = [[tk.Entry() for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                txt_input = ''
                if self.sudoku.board[i][j] != '0':
                    txt_input = self.sudoku.board[i][j]

                self.board_cells[i][j] = tk.Entry(
                    self.table,
                    width=4,
                    font=('Arial', 20),
                    borderwidth=0,
                    relief='ridge',
                    textvariable=tk.StringVar(
                        self.table, value=txt_input),
                    justify='center',
                )
                self.board_cells[i][j].grid(row=i, column=j)

                # change some 3x3 block cells
                if (i in (0, 1, 2, 6, 7, 8)) and (j in (0, 1, 2, 6, 7, 8)) or (i in (3, 4, 5) and j in (3, 4, 5)):
                    self.board_cells[i][j].config(bg='#f0f0f0')

        # algorithms dropdown menu
        self.algos_label = tk.StringVar(self, 'algorithm')
        self.algos_menu = tk.OptionMenu(
            self, self.algos_label, *self.sudoku.algorithms.keys())
        self.algos_menu.config(width=15)

        # board difficulty dropdown menu
        self.difficulty_label = tk.StringVar(self, 'medium')
        self.difficulty_menu = tk.OptionMenu(
            self, self.difficulty_label, *PREBUILT_BOARDS.keys(), command=lambda x: self.sudoku.update_board(self, x))
        self.difficulty_menu.config(width=15)

        # solve button
        self.solve_button = tk.Button(
            self,
            text='solve',
            command=lambda: (
                self.sudoku.solve(self, self.algos_label.get())
            )
        )
        self.solve_button.config(width=13)

        # display all elements in the app
        self.resizable(False, False)
        self.table.pack(fill='both', expand=True)
        self.algos_menu.pack(side=tk.LEFT, pady=5, padx=10)
        self.difficulty_menu.pack(side=tk.RIGHT, pady=5, padx=10)
        self.solve_button.pack(side=tk.TOP, pady=5)


def main():
    sudoku = Solver()
    SudokuApp(sudoku).mainloop()


if __name__ == '__main__':
    main()
