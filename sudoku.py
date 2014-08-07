# author: Kovrizhnykh Alexey

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import pprint
import copy

class Sudoku(QWidget):

    def __init__(self):
        super().__init__()
        self.check_trivial_steps = True
        self.fields = []
        self.setFixedSize(270 + 20, 300 + 20)
        for i in range(9):
            self.fields.append([])
            for j in range(9):
                self.fields[i].append(QLineEdit(self))
                self.fields[i][j].setGeometry(
                    i // 3 * 10 + 30 * i, j // 3 * 10 + 30 * j, 30, 30
                )
        self.clear_btn = QPushButton('Clear', self)
        self.clear_btn.setGeometry(0, 290, 145, 30)
        self.clear_btn.clicked.connect(self.clear_fields)
        self.solution_btn = QPushButton('Get solution', self)
        self.solution_btn.setGeometry(145, 290, 145, 30)
        self.solution_btn.clicked.connect(self.find_solution)

    def clear_fields(self):
        for i in range(9):
            for j in range(9):
                self.fields[i][j].setText('')

    def find_solution(self):
        gb = self.get_game_board()
        if not self.is_correct_board(gb):
            print('Incorrect game board')
            return
        if not self.get_solution(gb):
            print('Solution not found')
            return
        if not self.is_solution(gb):
            raise Exception('Program find solution, but it isn\'t correct')
        self.set_game_board(gb)
        print('Successful')

    def get_solution(self, gb):

        if self.is_solution(gb):
            return True

        possible_steps = self.get_possible_steps(gb)
        min = 10
        min_coord = (-1, -1)
        for i in range(9):
            for j in range(9):
                if possible_steps[i][j]:
                    if len(possible_steps[i][j]) < min:
                        min = len(possible_steps[i][j])
                        min_coord = (i, j)

        if min == 10:
            return False

        i, j = min_coord
        steps = possible_steps[i][j]
        for step in steps:
            gb_copy = copy.deepcopy(gb)
            gb_copy[i][j] = step
            if self.get_solution(gb_copy):
                for i in range(9):
                    for j in range(9):
                        gb[i][j] = gb_copy[i][j]
                return True
        return False

    def is_solution(self, gb):
        for i in range(9):
            for j in range(9):
                if gb[i][j] == 0:
                    return False
        return self.is_correct_board(gb)

    def get_possible_steps(self, gb):
        possible_steps = []
        for i in range(9):
            possible_steps.append([])
            for j in range(9):
                possible_steps[i].append(set(range(1, 10)))
        for i in range(9):
            for j in range(9):
                if gb[i][j] != 0:
                    possible_steps[i][j] = set()
                    for k in range(9):
                        if gb[i][j] in possible_steps[i][k]:
                            possible_steps[i][k].remove(gb[i][j])
                        if gb[i][j] in possible_steps[k][j]:
                            possible_steps[k][j].remove(gb[i][j])
                    row = i // 3
                    col = j // 3
                    for k in range(3):
                        for l in range(3):
                            x = row * 3 + k
                            y = col * 3 + l
                            if gb[i][j] in possible_steps[x][y]:
                                possible_steps[x][y].remove(gb[i][j])
        for i in range(3):
            for j in range(3):
                digital_counter = {}
                for k in range(1, 10):
                    digital_counter[k] = []
                for k in range(3):
                    for l in range(3):
                        x = i * 3 + k
                        y = j * 3 + l
                        for m in possible_steps[x][y]:
                            digital_counter[m].append((x, y))
                for k in range(1, 10):
                    if len(digital_counter[k]) == 1:
                        x, y = digital_counter[k][0]
                        possible_steps[x][y] = {k}
        return possible_steps

    def get_game_board(self):
        gb = []
        for i in range(9):
            gb.append([])
            for j in range(9):
                val = self.fields[j][i].text()
                try:
                    val = int(val)
                except ValueError:
                    val = 0
                gb[i].append(val)
        return gb

    def set_game_board(self, gb):
        for i in range(9):
            for j in range(9):
                if gb[j][i]:
                    self.fields[i][j].setText(str(gb[j][i]))
                else:
                    self.fields[i][j].setText('')

    def is_correct_board(self, gb):
        for i in range(9):
            for j in range(9):
                if gb[i][j] == 0:
                    continue
                if not (1 <= gb[i][j] <= 9):
                    return False
                for k in range(9):
                    if k != j and gb[i][j] == gb[i][k]:
                        return False
                    if k != i and gb[i][j] == gb[k][j]:
                        return False
                row = i // 3
                col = j // 3
                for k in range(3):
                    for l in range(3):
                        x = row * 3 + k
                        y = col * 3 + l
                        if x== i and y == j:
                            continue
                        if gb[x][y] == gb[i][j]:
                            return False
        return True

easy1 = (
    (0, 9, 0, 1, 8, 0, 0, 0, 0),
    (6, 3, 2, 0, 7, 0, 0, 0, 1),
    (8, 4, 1, 3, 0, 6, 0, 0, 2),
    (7, 0, 3, 0, 6, 0, 0, 0, 0),
    (2, 5, 8, 7, 0, 1, 6, 3, 9),
    (0, 0, 0, 0, 5, 0, 8, 0, 7),
    (1, 0, 0, 9, 0, 4, 2, 5, 8),
    (3, 0, 0, 0, 1, 0, 7, 6, 4),
    (0, 0, 0, 0, 2, 7, 0, 9, 0),
)

easy2 = (
    (0, 8, 6, 0, 1, 0, 0, 0, 0),
    (5, 0, 0, 0, 0, 0, 8, 7, 0),
    (0, 0, 0, 0, 8, 5, 2, 0, 0),
    (0, 1, 4, 9, 0, 0, 0, 0, 8),
    (0, 2, 0, 0, 0, 0, 0, 0, 0),
    (0, 9, 0, 6, 7, 0, 0, 5, 0),
    (0, 0, 2, 5, 6, 0, 0, 0, 3),
    (0, 0, 0, 7, 3, 4, 0, 0, 0),
    (0, 6, 0, 0, 2, 0, 1, 0, 5),
)

wiki1 = (
    (2, 0, 0, 0, 0, 5, 8, 9, 0),
    (0, 6, 0, 0, 9, 0, 7, 1, 0),
    (9, 0, 0, 7, 0, 0, 0, 0, 4),
    (0, 0, 0, 0, 6, 0, 4, 5, 8),
    (0, 0, 6, 0, 0, 0, 0, 0, 0),
    (5, 9, 0, 0, 3, 0, 0, 0, 0),
    (3, 0, 0, 0, 0, 8, 0, 0, 7),
    (0, 4, 9, 0, 2, 0, 0, 8, 0),
    (0, 8, 5, 1, 0, 0, 0, 0, 9),
)

wiki2 = (
    (0, 4, 0, 0, 8, 0, 0, 0, 7),
    (0, 0, 3, 7, 0, 2, 0, 0, 9),
    (0, 0, 0, 6, 3, 5, 0, 0, 0),
    (0, 7, 0, 0, 0, 0, 2, 0, 0),
    (9, 1, 0, 0, 0, 0, 0, 3, 8),
    (0, 0, 5, 0, 0, 0, 0, 7, 0),
    (0, 0, 0, 1, 2, 7, 0, 0, 0),
    (8, 0, 0, 4, 0, 3, 1, 0, 0),
    (2, 0, 0, 0, 5, 0, 0, 6, 0),
)

hard1 = (
    (0, 0, 5, 3, 0, 0, 0, 0, 0),
    (8, 0, 0, 0, 0, 0, 0, 2, 0),
    (0, 7, 0, 0, 1, 0, 5, 0, 0),
    (4, 0, 0, 0, 0, 5, 3, 0, 0),
    (0, 1, 0, 0, 7, 0, 0, 0, 6),
    (0, 0, 3, 2, 0, 0, 0, 8, 0),
    (0, 6, 0, 5, 0, 0, 0, 0, 9),
    (0, 0, 4, 0, 0, 0, 0, 3, 0),
    (0, 0, 0, 0, 0, 9, 7, 0, 0),
)

hard2 = (
    (0, 0, 0, 0, 8, 3, 9, 0, 0),
    (1, 0, 0, 0, 0, 0, 0, 3, 0),
    (0, 0, 4, 0, 0, 0, 0, 7, 0),
    (0, 4, 2, 0, 3, 0, 0, 0, 0),
    (6, 0, 0, 0, 0, 0, 0, 0, 4),
    (0, 0, 0, 0, 7, 0, 0, 1, 0),
    (0, 2, 0, 0, 0, 0, 0, 0, 0),
    (0, 8, 0, 0, 0, 9, 2, 0, 0),
    (0, 0, 0, 2, 5, 0, 0, 0, 6),
)

hard3 = (
    (8, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 3, 6, 0, 0, 0, 0, 0),
    (0, 7, 0, 0, 9, 0, 2, 0, 0),
    (0, 5, 0, 0, 0, 7, 0, 0, 0),
    (0, 0, 0, 0, 4, 5, 7, 0, 0),
    (0, 0, 0, 1, 0, 0, 0, 3, 0),
    (0, 0, 1, 0, 0, 0, 0, 6, 8),
    (0, 0, 8, 5, 0, 0, 0, 1, 0),
    (0, 9, 0, 0, 0, 0, 4, 0, 0),
)

empty_board = (
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0),
)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sudoku = Sudoku()
    sudoku.set_game_board(hard3)
    sudoku.show()
    app.exec()