# encoding:utf-8
import wx
import os
import random
import copy

ROWS = 4  # 设定游戏界面为4X4
COLS = 4


class MainWindow(wx.Window):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        # print("start the window")

        self.init_buffer()
        self.init_game()
        # self.set_menu()
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)

    # 初始化主界面
    def init_game(self):
        # print("init game")
        self.set_fonts()
        self.set_colors()
        self.high_score = 0
        self.cur_score = 0
        self.data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        # self.on_load_game()
        self.load_record()
        # print(self.high_score)
        self.next_step()
        self.next_step()
        self.draw_all()

    # 初始化缓存区
    def init_buffer(self):
        # print("the buffer")
        w, h = self.GetClientSize()
        self.buffer = wx.Bitmap(w, h)

    def on_size(self, event):
        # print("on_size")
        self.init_buffer()
        self.draw_all()

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)

    def set_fonts(self):
        self.bg_font = wx.Font(50, wx.SWISS, wx.NORMAL, wx.NORMAL, )
        self.score_font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.data_font = wx.Font(36, wx.ROMAN, wx.NORMAL, wx.NORMAL)

    def set_colors(self):
        self.score_color = (187, 163, 160)
        self.data_colors = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
                            16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114),
                            256: (237, 207, 114), 512: (237, 207, 114), 1024: (237, 207, 114), 2048: (237, 207, 114),
                            4096: (237, 207, 114), 8192: (237, 207, 114), 16384: (237, 207, 114),
                            32768: (237, 207, 114), 65536: (237, 207, 114), 131072: (237, 207, 114)}

    # 设置菜单栏
    def set_menu(self):
        # 创建菜单栏及菜单,并绑定监听器
        file_menu_bar = wx.MenuBar()
        self.SetMenuBar(file_menu_bar)
        file_menu = wx.Menu()
        file_menu_bar.Append(file_menu, u"菜单")

        menu_save_game = file_menu.Append(wx.ID_SAVE, "Save game")
        self.Bind(wx.EVT_MENU, self.on_save_game, menu_save_game, wx.ID_SAVE)

        menu_load_game = file_menu.Append(wx.ID_OPEN, "Load game")
        self.Bind(wx.EVT_MENU_OPEN, self.on_load_game, menu_load_game)

        file_menu.AppendSeparator()
        menu_exit = file_menu.Append(wx.ID_EXIT, "Exit game")
        self.Bind(wx.EVT_MENU_CLOSE, self.on_exit_game, menu_exit)

    # 游戏存档
    def on_save_game(self):
        data_str = ''
        for i in range(ROWS):
            for j in range(COLS):
                data_str += (str(self.data[i][j]) + '.')
        with open('gamefile.ini', 'w', encoding='utf-8')as fw:
            fw.write(data_str)

    # 游戏读档
    def on_load_game(self):
        if os.path.exists('gamefile.ini'):
            with open('gamefile.ini', 'r', encoding='utf-8')as fr:
                data_str = fr.read()
            data_list = data_str.split('.')
            for i in range(ROWS):
                for j in range(COLS):
                    self.data[i][j] = int(data_list[i * 4 + j])
            self.draw_all()
        else:
            wx.MessageDialog(self, u"没有存档", u"提示", style=wx.OK)

    # 退出游戏
    def on_exit_game(self, e):
        self.on_save_game()
        self.Close(True)

    # 读取最高分记录
    def load_record(self):
        if os.path.exists('record.ini'):
            with open('record.ini', 'r', encoding='utf-8')as fr:
                self.high_score = int(fr.read())

    # 存储新的最高分纪录
    def save_record(self):
        with open('record.ini', 'w', encoding='utf-8')as fw:
            fw.write(str(self.high_score))

    # 每次移动后随即生成一个方块
    def next_step(self):
        (i, j) = random.choice([(i, j) for i in range(ROWS) for j in range(COLS) if self.data[i][j] == 0])
        if random.randint(0, 1):
            self.data[i][j] = 2
        else:
            self.data[i][j] = 4

    # 绘制主界面
    def draw_all(self):
        # print("draw_all")
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.draw_bg(dc)
        self.draw_logo(dc)
        self.draw_hints(dc)
        self.draw_score(dc)
        self.draw_data(dc)
        # print("draw the game")

    # 绘制游戏背景
    def draw_bg(self, dc):
        dc.SetBackground(wx.Brush((250, 248, 239)))
        dc.Clear()
        dc.SetBrush(wx.Brush((187, 173, 160)))
        dc.SetPen(wx.Pen((187, 173, 160)))
        dc.DrawRoundedRectangle(15, 150, 475, 475, 5)

    def draw_logo(self, dc):
        dc.SetFont(self.bg_font)
        dc.SetTextForeground((119, 110, 101))
        dc.DrawText(u"2048", 15, 26)

    def draw_hints(self, dc):
        dc.SetFont(self.score_font)
        dc.SetTextForeground((119, 110, 101))
        dc.DrawText(u"合并相同数字，得到2048吧！", 15, 114)
        dc.DrawText(u"怎么玩：\n用上下左右箭头按键移动方块\n当相同数字的两个方块碰到一起时，会合成一个！", 15, 639)

    # 绘制游戏分数区域
    def draw_score(self, dc):
        dc.SetFont(self.score_font)
        cur_score_label_size = dc.GetTextExtent(u"得分")
        best_score_label_size = dc.GetTextExtent(u"最高分")
        cur_score_label_board = 15 * 2 + cur_score_label_size[0]
        best_score_label_board = 15 * 2 + best_score_label_size[0]
        cur_score_size = dc.GetTextExtent(str(self.cur_score))
        # print(self.high_score)
        best_score_size = dc.GetTextExtent(str(self.high_score))
        cur_score_board = 10 + cur_score_size[0]
        best_score_board = 10 + best_score_size[0]
        cur_score = max(cur_score_board, cur_score_label_board)
        best_score = max(best_score_board, best_score_label_board)
        dc.SetBrush(wx.Brush((187, 163, 160)))
        dc.SetPen(wx.Pen((187, 163, 160)))
        dc.DrawRoundedRectangle(505 - 15 - best_score, 40, best_score, 50, 3)
        dc.DrawRoundedRectangle(505 - 15 - best_score - 5 - cur_score, 40, cur_score, 50, 3)
        dc.SetTextForeground((238, 228, 218))
        dc.DrawText(u"最高分", 505 - 15 - best_score +
                    (best_score - best_score_label_size[0]) / 2, 48)
        dc.DrawText(u"得分", 505 - 15 - best_score - 5 - cur_score
                    + (cur_score - cur_score_label_size[0]) / 2, 48)
        dc.SetTextForeground((255, 255, 255))
        dc.DrawText(str(self.cur_score), 505 - 15 - best_score
                    + (best_score - best_score_size[0]) / 2, 68)
        dc.DrawText(str(self.cur_score),
                    505 - 15 - best_score - 5 - cur_score
                    + (cur_score - cur_score_size[0]) / 2, 68)

    # 绘制游戏区域
    def draw_data(self, dc):
        dc.SetFont(self.data_font)
        for row in range(ROWS):
            for col in range(COLS):
                data = self.data[row][col]
                data_color = self.data_colors[data]
                if data == 2 or data == 4:
                    dc.SetTextForeground((119, 110, 101))
                else:
                    dc.SetTextForeground((255, 255, 255))
                dc.SetBrush(wx.Brush(data_color))
                dc.SetPen(wx.Pen(data_color))
                dc.DrawRoundedRectangle(30 + col * 115, 165 + row * 115, 100, 100, 2)
                size = dc.GetTextExtent(str(data))
                while size[0] > 100 - 15 * 2:
                    self.data_font = wx.Font(self.data_font.GetPonitSize() * 4 / 5,
                                             wx.ROMAN, wx.NORMAL, wx.BOLD)
                    dc.SetFont(self.data_font)
                    size = dc.GetTextExtent(str(data))
                if data != 0:
                    dc.DrawText(str(data), 30 + col * 115 + (100 - size[0]) / 2,
                                165 + row * 115 + (100 - size[1]) / 2)

    # 读取到键盘输入
    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_UP:
            if self.can_move_up(self.data):
                self.on_move_up()
        elif key_code == wx.WXK_DOWN:
            if self.can_move_down(self.data):
                self.on_move_down()
        elif key_code == wx.WXK_LEFT:
            if self.can_move_left(self.data):
                self.on_move_left()
        elif key_code == wx.WXK_RIGHT:
            if self.can_move_right(self.data):
                self.on_move_right()

        self.is_new_record()
        self.next_step()
        self.is_game_over()
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.draw_data(dc)
        self.draw_score(dc)

    # 判断是否可以向上移动
    def can_move_up(self, data):
        for j in range(COLS):
            for i in range(ROWS - 1):
                if data[i][j] == 0 and data[i + 1][j] != 0:
                    return True
                if data[i][j] == data[i + 1][j] and data[i][j] != 0:
                    return True
        return False

    # 判断是否可以向下移动
    def can_move_down(self, data):
        for j in range(COLS):
            for i in range(ROWS - 1, 1, -1):
                if data[i][j] == 0 and data[i - 1][j] != 0:
                    return True
                if data[i][j] == data[i - 1][j] and data[i][j] != 0:
                    return True
        return False

    # 判断是否可以向左移动
    def can_move_left(self, data):
        for i in range(ROWS):
            for j in range(COLS - 1):
                if data[i][j] == 0 and data[i][j + 1] != 0:
                    return True
                if data[i][j] == data[i][j + 1] and data[i][j] != 0:
                    return True
        return False

    # 判断是否可以向右移动
    def can_move_right(self, data):
        for i in range(ROWS):
            for j in range(COLS - 1, 1, -1):
                if data[i][j] == 0 and data[i][j - 1] != 0:
                    return True
                if data[i][j] == data[i][j - 1] and data[i][j] != 0:
                    return True
        return False

    # 游戏向左移动
    def on_move_left(self):
        for i in range(ROWS):
            valid_datas = [self.data[i][j] for j in range(COLS) if self.data[i][j] != 0]
            if len(valid_datas) >= 2:
                num = 1
                while num < len(valid_datas):
                    if valid_datas[num - 1] == valid_datas[num]:
                        valid_datas[num - 1] *= 2
                        num += 1
                        if valid_datas[num - 1] > self.cur_score:
                            self.cur_score = valid_datas[num - 1]
                    num += 1
            for temp in range(COLS - len(valid_datas)):
                valid_datas.append(0)
            for j in range(COLS):
                self.data[i][j] = valid_datas[j]

    # 游戏向右移动
    def on_move_right(self):
        for i in range(ROWS):
            valid_datas = [self.data[i][j] for j in range(COLS) if self.data[i][j] != 0]
            if len(valid_datas) >= 2:
                num = len(valid_datas) - 1
                while num > 0:
                    if valid_datas[num] == valid_datas[num - 1]:
                        valid_datas[num] *= 2
                        num -= 1
                        if valid_datas[num] > self.cur_score:
                            self.cur_score = valid_datas[num]
                        del valid_datas[num - 1]
                    num -= 1
            for temp in range(COLS - len(valid_datas)):
                valid_datas.insert(0, 0)
            for j in range(COLS):
                self.data[i][j] = valid_datas[j]

    # 游戏向上移动
    def on_move_up(self):
        for j in range(COLS):
            valid_datas = [self.data[i][j] for i in range(ROWS) if self.data[i][j] != 0]
            if len(valid_datas) >= 2:
                num = 1
                while num < len(valid_datas):
                    if valid_datas[num] == valid_datas[num - 1]:
                        valid_datas[num - 1] *= 2
                        num += 1
                        if valid_datas[num] > self.cur_score:
                            self.cur_score = valid_datas[num]
                        del valid_datas[num]
                    num += 1
            for temp in range(ROWS - len(valid_datas)):
                valid_datas.append(0)
            for i in range(ROWS):
                self.data[i][j] = valid_datas[i]

    # 游戏向下移动
    def on_move_down(self):
        for j in range(COLS):
            valid_datas = [self.data[i][j] for i in range(ROWS) if self.data[i][j] != 0]
            if len(valid_datas) >= 2:
                num = len(valid_datas) - 1
                while num > 0:
                    if valid_datas[num] == valid_datas[num - 1]:
                        valid_datas[num] *= 2
                        if valid_datas[num] > self.cur_score:
                            self.cur_score = valid_datas[num]
                        del valid_datas[num - 1]
                        num -= 1
                    num -= 1
            for temp in range(ROWS - len(valid_datas)):
                valid_datas.insert(0, 0)
            for i in range(ROWS):
                self.data[i][j] = valid_datas[i]

    # 若打破最高分的纪录，存储新的纪录
    def is_new_record(self):
        if self.cur_score > self.high_score:
            self.high_score = self.cur_score
            self.save_record()
            wx.MessageDialog(None, u"新纪录 " + str(self.high_score), style=wx.OK or wx.ICON_INFORMATION)

    # 判断游戏结束
    def is_game_over(self):
        if not self.can_move_left(self.data) and not self.can_move_right(self.data) \
                and not self.can_move_up(self.data) and not self.can_move_down(self.data):
            dlg = wx.MessageDialog(None, u"游戏结束，再来一局？", style=wx.YES_NO or wx.YES_DEFAULT or wx.ICON_QUESTION)
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                self.init_game()
            # elif result == wx.ID_NO:
            #     self.on_exit_game()
            dlg.Destroy()
        else:
            return


class Frame(wx.Frame):
    def __init__(self, title):
        super(Frame, self).__init__(None, -1, title, style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^
                                                           wx.RESIZE_BORDER)
        # print("start the frame")
        self.SetIcon(wx.Icon('icon.jpg'))
        self.window = MainWindow(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.window.on_save_game()
        self.Destroy()


class APP(wx.App):
    def on_init(self):
        self.frame = Frame(title=u"2048 v1.0 by hb")
        # print("start the app")
        self.frame.SetClientSize((505, 720))
        self.frame.Center()
        self.frame.Show(True)
        return True


if __name__ == '__main__':
    app = wx.App()
    app.frame = Frame(title=u"2048 v1.0 by hb")
    app.frame.SetClientSize((505, 720))
    app.frame.Center()
    app.frame.Show(True)
    app.MainLoop()
