import urllib.request
import re
import sudoku

digit_re = re.compile(
    r'<INPUT NAME=cheat ID="cheat" TYPE=hidden VALUE="(\d+)">'
)
visible_re = re.compile(
    r'<INPUT ID="editmask" TYPE=hidden VALUE="(\d+)">'
)

gb = [[0 for i in range(9)] for j in range(9)]

game = sudoku.Sudoku(3, False)

for i in range(0, 100):
    content = urllib.request.urlopen(
        "http://show.websudoku.com/?level=3&set_id=" + str(i)
    ).read().decode()
    digs = re.findall(digit_re, content)[0]
    visible = re.findall(visible_re, content)[0]
    for j in range(81):
        x = j // 9
        y = j - 9 * x
        if visible[j] == '0':
            gb[x][y] = int(digs[j])
        else:
            gb[x][y] = 0
    file_name = 'websudoku_com_evil_{:03d}.sudokugb'.format(i)
    print(file_name)
    game.save_gb_to_file('tests_new/' + file_name, gb)
