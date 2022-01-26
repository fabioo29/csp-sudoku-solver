import time


class Solver(object):
    """class to solve the sudoku board"""

    def __init__(self):
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

    def board_init(self):
        """initializes the sudoku board"""
        return [
            ['0', '0', '2'] + ['0', '3', '0'] + ['0', '0', '8'],
            ['0', '0', '0'] + ['0', '0', '8'] + ['0', '0', '0'],
            ['0', '3', '1'] + ['0', '2', '0'] + ['0', '0', '0'],
            # -------------------------------------------------
            ['0', '6', '0'] + ['0', '5', '0'] + ['2', '7', '0'],
            ['0', '1', '0'] + ['0', '0', '0'] + ['0', '5', '0'],
            ['2', '0', '4'] + ['0', '6', '0'] + ['0', '3', '1'],
            # -------------------------------------------------
            ['0', '0', '0'] + ['0', '8', '0'] + ['6', '0', '5'],
            ['0', '0', '0'] + ['0', '0', '0'] + ['0', '1', '3'],
            ['0', '0', '5'] + ['3', '1', '0'] + ['4', '0', '0']
        ]

    def getNextLocation(self):
        """get next empty cell on the board"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == '0':
                    return (i, j)
        return (-1, -1)

    def isValid(self, row: int, col: int, num: int):
        """checks if the number is valid in the row, column and 3x3 square"""
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
                cpy = self.rv[:]
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

    def solve(self, method: str = 'csp_backtracking'):
        """solves the sudoku board with a given method"""
        self.iteration = 0
        self.board = self.board_init()
        if method == 'csp_backtracking':
            self.rv = self.getDomain()
        start = time.time()
        self.algorithms[method]()
        elapsed = time.time() - start
        print(
            method,
            f'| iterations: {self.iteration}',
            f'| time taken: {elapsed:.2f}s'
        )


def main():
    sudoku = Solver()
    sudoku.solve('backtracking')
    sudoku.solve('csp_backtracking')


if __name__ == '__main__':
    main()
