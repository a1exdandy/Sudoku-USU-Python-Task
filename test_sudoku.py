# Author: Kovrizhnykh Alexey
# Тестовый модуль для Sudoku

import unittest
from sudoku import Sudoku

# Набор из нескольких состояние игрового поля Судоку размера
# 9 x 9 разной сложности
easy1 = [
    [0, 9, 0, 1, 8, 0, 0, 0, 0],
    [6, 3, 2, 0, 7, 0, 0, 0, 1],
    [8, 4, 1, 3, 0, 6, 0, 0, 2],
    [7, 0, 3, 0, 6, 0, 0, 0, 0],
    [2, 5, 8, 7, 0, 1, 6, 3, 9],
    [0, 0, 0, 0, 5, 0, 8, 0, 7],
    [1, 0, 0, 9, 0, 4, 2, 5, 8],
    [3, 0, 0, 0, 1, 0, 7, 6, 4],
    [0, 0, 0, 0, 2, 7, 0, 9, 0],
]

easy2 = [
    [0, 8, 6, 0, 1, 0, 0, 0, 0],
    [5, 0, 0, 0, 0, 0, 8, 7, 0],
    [0, 0, 0, 0, 8, 5, 2, 0, 0],
    [0, 1, 4, 9, 0, 0, 0, 0, 8],
    [0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 0, 6, 7, 0, 0, 5, 0],
    [0, 0, 2, 5, 6, 0, 0, 0, 3],
    [0, 0, 0, 7, 3, 4, 0, 0, 0],
    [0, 6, 0, 0, 2, 0, 1, 0, 5],
]

wiki1 = [
    [2, 0, 0, 0, 0, 5, 8, 9, 0],
    [0, 6, 0, 0, 9, 0, 7, 1, 0],
    [9, 0, 0, 7, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 6, 0, 4, 5, 8],
    [0, 0, 6, 0, 0, 0, 0, 0, 0],
    [5, 9, 0, 0, 3, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 8, 0, 0, 7],
    [0, 4, 9, 0, 2, 0, 0, 8, 0],
    [0, 8, 5, 1, 0, 0, 0, 0, 9],
]

wiki2 = [
    [0, 4, 0, 0, 8, 0, 0, 0, 7],
    [0, 0, 3, 7, 0, 2, 0, 0, 9],
    [0, 0, 0, 6, 3, 5, 0, 0, 0],
    [0, 7, 0, 0, 0, 0, 2, 0, 0],
    [9, 1, 0, 0, 0, 0, 0, 3, 8],
    [0, 0, 5, 0, 0, 0, 0, 7, 0],
    [0, 0, 0, 1, 2, 7, 0, 0, 0],
    [8, 0, 0, 4, 0, 3, 1, 0, 0],
    [2, 0, 0, 0, 5, 0, 0, 6, 0],
]

hard1 = [
    [0, 0, 5, 3, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 0, 0, 2, 0],
    [0, 7, 0, 0, 1, 0, 5, 0, 0],
    [4, 0, 0, 0, 0, 5, 3, 0, 0],
    [0, 1, 0, 0, 7, 0, 0, 0, 6],
    [0, 0, 3, 2, 0, 0, 0, 8, 0],
    [0, 6, 0, 5, 0, 0, 0, 0, 9],
    [0, 0, 4, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 9, 7, 0, 0],
]

hard2 = [
    [0, 0, 0, 0, 8, 3, 9, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 4, 0, 0, 0, 0, 7, 0],
    [0, 4, 2, 0, 3, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 7, 0, 0, 1, 0],
    [0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 8, 0, 0, 0, 9, 2, 0, 0],
    [0, 0, 0, 2, 5, 0, 0, 0, 6],
]

hard3 = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0],
]

empty_board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]


class SudokuTestCase(unittest.TestCase):

    def test_easy1(self):
        sudoku = Sudoku(3, False)
        sudoku.get_solution(easy1)
        self.assertTrue(sudoku.is_solution(easy1))

    def test_easy2(self):
        sudoku = Sudoku(3, False)
        sudoku.get_solution(easy2)
        self.assertTrue(sudoku.is_solution(easy2))

    def test_wiki1(self):
        sudoku = Sudoku(3, False)
        sudoku.get_solution(wiki1)
        self.assertTrue(sudoku.is_solution(wiki1))

    def test_wiki2(self):
        sudoku = Sudoku(3, False)
        sudoku.get_solution(wiki2)
        self.assertTrue(sudoku.is_solution(wiki2))

    def test_hard1(self):
        sudoku = Sudoku(3, False)
        sudoku.get_solution(hard1)
        self.assertTrue(sudoku.is_solution(hard1))

    def test_hard2(self):
        sudoku = Sudoku(3, False)
        sudoku.get_solution(hard2)
        self.assertTrue(sudoku.is_solution(hard2))

    def test_hard3(self):
        sudoku = Sudoku(3, False)
        sudoku.get_solution(hard3)
        self.assertTrue(sudoku.is_solution(hard3))

if __name__ == '__main__':
    unittest.main()
