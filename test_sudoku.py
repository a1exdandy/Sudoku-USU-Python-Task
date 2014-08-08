# Author: Kovrizhnykh Alexey
# Тестовый модуль для Sudoku

import unittest
from sudoku import Sudoku
from pathlib import Path


TESTDIR = 'tests'


class SudokuTestCase(unittest.TestCase):

    def setUp(self):
        self.sudoku = Sudoku(3, False)


def gen_test(file_name):
    """Функция генерирует тест-case из файла
    """
    in_file = open(file_name)
    size = int(in_file.readline())
    in_file.close()
    sudoku = Sudoku(size, False)
    gb = sudoku.load_gb_from_file(file_name)

    def test_func(self):
        self.assertTrue(self.sudoku.get_solution(gb))
        self.assertTrue(self.sudoku.is_solution(gb))

    return test_func

# Перебираем все файлы в директории TESTDIR и для каждого
# генерируем новый тест-case в классе юнит-теста
path = Path(TESTDIR)
for file in path.iterdir():
    file_name = file.name
    test_case_name = 'test_' + file_name.split('.')[0]
    setattr(
        SudokuTestCase,
        test_case_name,
        gen_test(TESTDIR + '/' + file_name)
    )

if __name__ == '__main__':
    unittest.main()
