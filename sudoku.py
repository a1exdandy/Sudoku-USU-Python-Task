# author: Kovrizhnykh Alexey

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
import copy


class Sudoku(QMainWindow):
    """Основной класс программы. реализцющий интерфейс пользователя.
    Содержит методы для работы с задачами-судоку (проверка
    корректности поля, метод для поиска решения и т.д.).
    """

    def __init__(self, size, ui=True):
        """Конструктор класса Sudoku для решения задач-судоку на
        игровом поле размера size ^ 2 на size ^ 2, при  необходимости
        производит построение интерфейса для работы интерактивной
        работы
        """
        self.size = size
        # n - это размер поля, а также максимальное возможное число в
        # в клетке поля. Определяется в этом месте для более понятного
        # и простого кода далее
        n = size ** 2

        # Завершаем инициализацию, если интерфейс не нужен
        if not ui:
            return
        # Инициализация подкласса QWidget
        super().__init__()
        # Создаем меню для работы с файлами
        file_menu = self.menuBar().addMenu('File')
        # Загрузка
        open_action = QAction('Open', self)
        open_action.setShortcuts(QKeySequence.Open)
        open_action.triggered.connect(self.show_load_dialog)
        file_menu.addAction(open_action)
        # Сохранение
        save_action = QAction('Save', self)
        save_action.setShortcuts(QKeySequence.Save)
        save_action.triggered.connect(self.show_save_dialog)
        file_menu.addAction(save_action)
        # Выход
        quit_action = QAction('Quit', self)
        quit_action.setShortcuts(QKeySequence.Quit)
        quit_action.triggered.connect(exit)
        file_menu.addAction(quit_action)
        # Создаем меню редактирования
        edit_menu = self.menuBar().addMenu('Edit')
        # Отмена
        undo_action = QAction('Undo', self)
        undo_action.setShortcuts(QKeySequence.Undo)
        undo_action.triggered.connect(self.undo_last_change)
        edit_menu.addAction(undo_action)
        # "Отмена отмены" =D
        redo_action = QAction('Redo', self)
        redo_action.setShortcuts(QKeySequence.Redo)
        redo_action.triggered.connect(self.redo_last_change)
        edit_menu.addAction(redo_action)
        # Создаем меню справки
        help_menu = self.menuBar().addMenu('Help')
        # О программе
        about_action = QAction('About...', self)
        about_action.triggered.connect(self.show_about_message_box)
        help_menu.addAction(about_action)
        # Создаем центральный виджет, в котором будут находится
        # текстовые поля для редактирования и кнопки отчистки
        # и поиска решения
        central_widget = QWidget(self)
        # fields - двумерный массив, который будет заполнен текстовыми
        # полями для редактирования игрового поля Судоку
        self.fields = []
        # Вычисление ширины окна. Каждое текстовое поле будет иметь
        # ширину 30пикс. Также учитывается разрыв (10пикс) между блоками
        # размера size на size. (Их ровно size - 1)
        width = n * 30 + (size - 1) * 10
        # Высота вычисляется аналогично, но с учетом дополнительного
        # места для кнопок управления
        height = n * 30 + (size - 1) * 10 + 30
        central_widget.setFixedSize(width, height)
        # Заполняем двумерный массив ссылками на текстовые поля
        for i in range(n):
            self.fields.append([])
            for j in range(n):
                self.fields[i].append(QLineEdit(central_widget))
                # Прибавка i // size * 10 и j // size * 10 нужны для
                # создания отступа между блоками размера size на size
                self.fields[i][j].setGeometry(
                    i // size * 10 + 30 * i,
                    j // size * 10 + 30 * j,
                    30, 30
                )
        # clear_btn - кнопка для отчистки игрового поля Судоку
        self.clear_btn = QPushButton('Clear', central_widget)
        self.clear_btn.setGeometry(0, height - 30, width // 2, 30)
        self.clear_btn.clicked.connect(self.clear_fields)
        # solution_btn - кнопка для запуска процесса поиска
        # решеня для задачи
        self.solution_btn = QPushButton('Get solution', central_widget)
        self.solution_btn.setGeometry(width // 2, height - 30, width // 2, 30)
        self.solution_btn.clicked.connect(self.find_solution)
        # Назначем центральный виджет главному окну программы
        self.setCentralWidget(central_widget)
        self.layout().setSizeConstraint(QLayout.SetFixedSize)

    def show_load_dialog(self):
        """Метод, предоставляющий диалог выбора файла для загрузки
        состояния игрового поля.
        """
        file_name, file_type = QFileDialog.getOpenFileName(
            self,
            'Load game board', '',
            'Sudoku game board file (*.sudokugb)'
        )
        gb = self.load_gb_from_file(file_name)
        self.set_game_board(gb)

    def load_gb_from_file(self, file_name):
        """Метод, загружающий состояние поля из файла
        """
        load_file = open(file_name, 'r')
        size = int(load_file.readline())
        if size != self.size:
            print('Error size')
            load_file.close()
            return
        n = size ** 2
        gb = []
        for i in range(n):
            gb.append([])
            line = load_file.readline().split(' ')
            for j in range(n):
                gb[i].append(int(line[j]))
        load_file.close()
        return gb

    def show_save_dialog(self):
        """Метод, предоставляющий диалог выбора файла для сохранения
        состояния игрового поля.
        """
        file_name, file_type = QFileDialog.getSaveFileName(
            self,
            'Save game board', '',
            'Sudoku game board file (*.sudokugb)'
        )
        gb = self.get_game_board()
        self.save_gb_to_file(file_name, gb)

    def save_gb_to_file(self, file_name, gb):
        """Метод, сохраняющий текущее состояние поля в файле
        """
        save_file = open(file_name, 'w')
        save_file.write(str(self.size) + '\n')
        n = self.size ** 2
        for i in range(n):
            for j in range(n):
                save_file.write(str(gb[i][j]) + ' ')
            save_file.write('\n')
        save_file.close()

    def undo_last_change(self):
        pass

    def redo_last_change(self):
        pass

    def show_about_message_box(self):
        pass

    def clear_fields(self):
        """Метод для отчистки текущего сотояния поля
        """
        n = self.size ** 2
        for i in range(n):
            for j in range(n):
                self.fields[i][j].setText('')

    def find_solution(self):
        """Метод, запускающий поиск решения для текущего состояния
        ирового поля. Запускается при нажатии на кнопку Get Solution
        """
        # Получаем двумерный массив на основе текущего состояний
        # текстовых полей
        gb = self.get_game_board()
        # Проверка на корректность входных данных
        if not self.is_correct_board(gb):
            print('Incorrect game board')
            return
        # Поиск решения. Если каким-то образом решение не было найдено,
        # сообщаем это пользователю
        if not self.get_solution(gb):
            print('Solution not found')
            return
        # Проверяем, действительно ли мы нашли решение
        if not self.is_solution(gb):
            raise Exception('Program find solution, but it isn\'t correct')
        # Выводим решение на экран
        self.set_game_board(gb)

    def get_solution(self, gb):
        """Метод, выполняющий поиск решения поля, заданного двумерным
        массивом gb.
        Алгоритм поиска следующий:
        1) Если решение уже найдено, возвращаем True
        2) Получаем массив со всеми возможными ходами и ищем в нем
           поле с минимальным колличеством доступных ходов.
        3) Для каждого хода создаем копию игрового поля и рекурсивно
           запускаем данный процесс для этой копии. Если для очередного
           хода было найдено решение, копируем копию в исходной массив и
           возвращаем True
        """

        # Проверяем, найденно ли уже решение
        if self.is_solution(gb):
            return True

        # n - размер игрового поля и максимально число в клетке
        n = self.size ** 2
        # получаем массив доступных ходов для поля
        # см. описание метода get_possible_steps(gb)
        possible_steps = self.get_possible_steps(gb)

        # Ищем клетку с минимальным количеством возможных ходов.
        # Присваиваем переменно min заведомо такое значение,
        # больше которого на поле нет (n + 1)
        min = n + 1
        # В min_coord будем запоминать найденное поле
        min_coord = (-1, -1)
        for i in range(n):
            for j in range(n):
                # Не обновляем переменную min, если ходов в клетке (i, j)
                # нет (пустой set, значение длины 0)
                if possible_steps[i][j]:
                    if len(possible_steps[i][j]) < min:
                        min = len(possible_steps[i][j])
                        min_coord = (i, j)

        # Если доступных ходов небыло найдено, выходим
        if min == n + 1:
            return False

        # Начинаем перебирать возможные ходы.
        i, j = min_coord
        steps = possible_steps[i][j]
        for step in steps:
            # Для очередного хода создаем копию исхоного игрового поля,
            # чтобы его не портить
            gb_copy = copy.deepcopy(gb)
            gb_copy[i][j] = step
            # Если решение было найдено, копируем его в исходной массив
            # и возвращаем True
            if self.get_solution(gb_copy):
                for i in range(n):
                    for j in range(n):
                        gb[i][j] = gb_copy[i][j]
                return True
        # Если решение не было найдено, возвращаем False
        return False

    def is_solution(self, gb):
        """ Метод, проверяющий, является ли состояние игрового поля,
        записанное в двкхмерном массиве gb решением.
        """
        # Будем считать состояние игрового поля решением, если
        # все его ячейки отличны от нуля и поле заполнено корректно
        n = self.size ** 2
        for i in range(n):
            for j in range(n):
                if gb[i][j] == 0:
                    return False
        # Проверка на корректность поля
        return self.is_correct_board(gb)

    def get_possible_steps(self, gb):
        """ Метод, возвращающий двухмерный массив возможных ходов для
        текущего состояния игрового поля gb в соответствии с правилами
        Судоку: числа в строчках, в столбцах и в блоках размера
        size на size не могут повторятся. Результат представляет собой
        двухмерный массив, в i, j ячейке которого хранится множество
        возможных ходов.
        """
        n = self.size ** 2
        possible_steps = []
        # Изначално удем считать, что доступны абсолютно все ходы
        # (от 1 до n в каждой ячейке). В дальнейщем будем вычеркивать
        # недопустимые ходы.
        for i in range(n):
            possible_steps.append([])
            for j in range(n):
                possible_steps[i].append(set(range(1, n + 1)))
        for i in range(n):
            for j in range(n):
                # Если ячейка i, j заполнена, счтаем, что для неё нет
                # ходов (пустое множество)
                if gb[i][j] != 0:
                    possible_steps[i][j] = set()
                    # После чего вычеркиваем число в текучей ячейки
                    # из строки и столбца, в которой назодится ячйека,
                    # а также из блока размера size на size, которому
                    # ячейка принадлежит
                    for k in range(n):
                        if gb[i][j] in possible_steps[i][k]:
                            possible_steps[i][k].remove(gb[i][j])
                        if gb[i][j] in possible_steps[k][j]:
                            possible_steps[k][j].remove(gb[i][j])
                    # Вычисляем координаты блока
                    row = i // self.size
                    col = j // self.size
                    for k in range(self.size):
                        for l in range(self.size):
                            # Вычисляем координаты ячейки в блоке
                            x = row * self.size + k
                            y = col * self.size + l
                            if gb[i][j] in possible_steps[x][y]:
                                possible_steps[x][y].remove(gb[i][j])
        # После всех проделанных действий считаем числа в каждом блоке,
        # и если какое-то из них встречается в единственной ячейке,
        # то в ней не может быть других ходовом, кромой этого числа.
        for i in range(self.size):
            for j in range(self.size):
                digital_counter = {}
                for k in range(1, n + 1):
                    digital_counter[k] = []
                for k in range(self.size):
                    for l in range(self.size):
                        x = i * self.size + k
                        y = j * self.size + l
                        for m in possible_steps[x][y]:
                            digital_counter[m].append((x, y))
                for k in range(1, n + 1):
                    if len(digital_counter[k]) == 1:
                        x, y = digital_counter[k][0]
                        possible_steps[x][y] = {k}
        # Тоже самое проделываем для строк и стлбцев
        for i in range(n):
            # Проверка для i-ой строки
            digital_counter = {}
            for j in range(1, n + 1):
                digital_counter[j] = []
            for j in range(n):
                for k in possible_steps[i][j]:
                    digital_counter[k].append((i, j))
            for j in range(1, n + 1):
                if len(digital_counter[j]) == 1:
                    x, y = digital_counter[j][0]
                    possible_steps[x][y] = {j}
            # Проверка для i-ого столбца
            digital_counter = {}
            for j in range(1, n + 1):
                digital_counter[j] = []
            for j in range(n):
                for k in possible_steps[j][i]:
                    digital_counter[k].append((j, i))
            for j in range(1, n + 1):
                if len(digital_counter[j]) == 1:
                    x, y = digital_counter[j][0]
                    possible_steps[x][y] = {j}
        # Возвращаем результат
        return possible_steps

    def get_game_board(self):
        """Метод возвращает двухмерный массив на основе ткущего состояния
        текстовых полей.
        """
        n = self.size ** 2
        gb = []
        for i in range(n):
            gb.append([])
            for j in range(n):
                val = self.fields[j][i].text()
                # Будем считать пустую ячейку поля нулем (0)
                try:
                    val = int(val)
                except ValueError:
                    val = 0
                gb[i].append(val)
        return gb

    def set_game_board(self, gb):
        """Метод заполняет текстовые поля на основе данных из двумерного
        масива, задающего состояние игрового поля.
        """
        n = self.size ** 2
        for i in range(n):
            for j in range(n):
                if gb[j][i]:
                    self.fields[i][j].setText(str(gb[j][i]))
                else:
                    self.fields[i][j].setText('')

    def is_correct_board(self, gb):
        """Метод проверят, является ли состояние игрового поля, заданного
        двухмерным массивом gb, корректным (на основе правил Судоку, см.
        описание метода get_possible_steps(gb))
        """
        n = self.size ** 2
        for i in range(n):
            for j in range(n):
                if gb[i][j] == 0:
                    continue
                if not (1 <= gb[i][j] <= n):
                    return False
                for k in range(n):
                    if k != j and gb[i][j] == gb[i][k]:
                        return False
                    if k != i and gb[i][j] == gb[k][j]:
                        return False
                row = i // self.size
                col = j // self.size
                for k in range(self.size):
                    for l in range(self.size):
                        x = row * self.size + k
                        y = col * self.size + l
                        if x == i and y == j:
                            continue
                        if gb[x][y] == gb[i][j]:
                            return False
        return True

# Начальное состояние поля размера 9x9 для демонстрации работы
sample = (
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Создаем новый интерфейс для работы с игровым полем 9x9
    sudoku = Sudoku(3)
    # Устанавливаем начальное состояние игрового поля
    sudoku.set_game_board(sample)
    sudoku.show()
    app.exec()
