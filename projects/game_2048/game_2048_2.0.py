# -*-coding=utf-8-*-
import curses
from random import randrange, choice
from collections import defaultdict

actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Quit']
letter_codes = [ord(char) for char in 'WASDRQwasdrq']
actions_dict = dict(zip(letter_codes, actions * 2))


def get_user_action(keyboard):  # 获取用户输入
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]


def transpose(field):  # 矩阵转置
    return [list(row) for row in zip(*field)]


def invert(field):  # 矩阵逆转
    return [row[::-1] for row in field]


class GameField(object):  # 创建棋盘
    def __init__(self, height=4, width=4, win=2048):
        self.height = height
        self.width = width
        self.win_score = win
        self.instant_score = 0
        self.top_score = 0
        self.reset()

    def reset(self):  # 重置棋盘
        if self.instant_score > self.top_score:
            self.top_score = self.instant_score
        self.instant_score = 0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        self.spawn()  # 生成初始的两个格子
        self.spawn()

    def spawn(self):  # 随机生成下一步出现的数字2或4
        new_element = 4 if randrange(100) > 69 else 2
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def can_move(self, direction):  # 判断是否可以移动
        def can_move_left(row):
            def judge(i):
                if row[i] == 0 and row[i + 1] != 0:
                    return True
                if row[i] != 0 and row[i] == row[i + 1]:
                    return True
                return False

            return any(judge(i) for i in range(len(row) - 1))

        check = {}
        check['Left'] = lambda field: any(can_move_left(row) for row in field)
        check['Right'] = lambda field: check['Left'](invert(field))
        check['Up'] = lambda field: check['Left'](transpose(field))
        check['Down'] = lambda field: check['Right'](transpose(field))
        if direction in check:
            return check[direction](self.field)
        else:
            return False

    def move(self,direction):  # 上下左右移动

        def move_row_left(row):  # 向左移动合并

            def move(row):  # 移动非0单元
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row):  # 合并邻近元素

                flag = False
                new_row = []
                for i in range(len(row)):
                    if flag:
                        new_row.append(0)
                        flag = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            new_row.append(2 * row[i])
                            if 2 * row[i] > self.instant_score:
                                self.instant_score = 2 * row[i]
                            flag = True
                        else:
                            new_row.append(row[i])

                return new_row

            return move(merge(move(row)))

        moves = {}
        moves['Left'] = lambda field: [move_row_left(row) for row in field]
        moves['Right'] = lambda field: invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field: transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field: transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.can_move(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    def is_win(self):  # 判断游戏胜利
        return self.instant_score >= self.win_score

    def is_gameover(self):  # 判断游戏结束
        return not any([self.can_move(direction) for direction in actions[:4]])

    def draw(self, screen):  # # 绘制界面
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart   (Q)Quit     '
        gameover_string = '        Game Over!!!          '
        win_string = '         You Win!!!           '

        def cast(string):
            screen.addstr(string + '\n')

        def draw_line():  # 画行之间间隔的线
            line = '+' + ('------+' * self.width)
            separator = defaultdict(lambda: line)

            if not hasattr(draw_line, "counter"):
                draw_line.counter = 0
            cast(separator[draw_line.counter])
            draw_line.counter += 1

        def draw_row(row):  # 画行
            cast("".join('|{:^6}'.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.instant_score))
        if 0 != self.top_score:
            cast('TOP_SCORE: ' + str(self.top_score))

        for row in self.field:
            draw_line()
            draw_row(row)

        draw_line()

        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)


def main(stdscr):
    def init():
        # 初始化游戏界面  -->完成
        field.reset()
        return 'Gaming'

    def game():
        # 绘制游戏界面   -->完成
        field.draw(stdscr)
        action = get_user_action(stdscr)  # 用户输入操作     -->完成
        if action == 'Restart':
            return 'Init'
        if action == 'Quit':
            return 'Quit'
        if field.move(action):
            if field.is_win():  # 胜利条件 -->完成
                return 'Win'
            if field.is_gameover():  # 败条件   -->完成
                return 'Fail'
        return 'Gaming'  # 游戏继续

    def not_game(state):
        # 根据状态绘制游戏胜利或失败界面  -->完成
        field.draw(stdscr)
        action = get_user_action(stdscr)  # 用户输入 -->完成
        # 除非用户输入Restart或Quit，其他输入动作不改变当前状态
        responses = defaultdict(lambda: state)
        responses['Restart'], responses['Quit'] = 'Init', 'Quit'
        return responses[action]

    # 根据状态返回相应函数，对出相应的动作
    state_action = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'GameOver': lambda: not_game('GameOver'),
        'Gaming': game
    }
    curses.use_default_colors()
    field = GameField()
    state = 'Init'
    while state != 'Quit':
        state = state_action[state]()

if __name__ == '__main__':
    curses.wrapper(main)
