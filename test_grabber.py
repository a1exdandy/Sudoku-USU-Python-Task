import urllib.request
import re
import sudoku

digit_re = re.compile(
    r'<INPUT NAME=cheat ID="cheat" TYPE=hidden VALUE="(\d+)">'
)
visible_re = re.compile(
    r'<INPUT ID="editmask" TYPE=hidden VALUE="(\d+)">'
)

gb = [[0] * 9] * 9

game = sudoku.Sudoku(3, False)

for i in range(0, 100):
    content = urllib.request.urlopen(
        "http://show.websudoku.com/?level=3&set_id=" + str(i)
    ).read().decode()
    digs = re.findall(digit_re, content)[0]
    visible = re.findall(visible_re, content)[0]
    for j in range(81):
        if visible[j] == '0':
            gb[j // 9][j % 9] = int(digs[j])
        else:
            gb[j // 9][j % 9] = 0
    print('websudoku_com_evil_' + str(i).zfill(3))
    game.save_gb_to_file('tests/websudoku_com_hard_' + str(i).zfill(3), gb)
