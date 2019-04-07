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
        w, h = self.GetClientSize()
        self.buffer = wx.Bitmap(w, h)

    def on_size(self, event):
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

    # 退出游戏
    def on_exit_game(self):
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
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
        self.draw_bg(dc)
        self.draw_logo(dc)
        self.draw_hints(dc)
        self.draw_score(dc)
        self.draw_data(dc)

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
        dc.DrawText(str(self.high_score), 505 - 15 - best_score
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
                # while size[0] > 100 - 15 * 2:
                #     self.data_font = wx.Font(self.data_font.GetPonitSize() * 4 / 5,
                #                              wx.ROMAN, wx.NORMAL, wx.BOLD)
                #     dc.SetFont(self.data_font)
                #     size = dc.GetTextExtent(str(data))
                if data != 0:
                    dc.DrawText(str(data), 30 + col * 115 + (100 - size[0]) / 2,
                                165 + row * 115 + (100 - size[1]) / 2)

    # 读取到键盘输入
    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_UP:
            self.do_move(self.move_up_down(True))
        elif key_code == wx.WXK_DOWN:
            self.do_move(self.move_up_down(False))
        elif key_code == wx.WXK_LEFT:
            self.do_move(self.move_left_right(True))
        elif key_code == wx.WXK_RIGHT:
            self.do_move(self.move_left_right(False))

    def update(self, data_list, direction):
        score = 0
        if direction:
            i = 1
            while i < len(data_list):
                if data_list[i - 1] == data_list[i]:
                    del data_list[i]
                    data_list[i - 1] *= 2
                    if data_list[i - 1] > score:
                        score = data_list[i - 1]
                    i += 1
                i += 1
        else:
            i = len(data_list) - 1
            while i > 0:
                if data_list[i - 1] == data_list[i]:
                    del data_list[i - 1]
                    data_list[i - 1] *= 2
                    if data_list[i - 1] > score:
                        score = data_list[i - 1]
                    i -= 1
                i -= 1
        return score

    def move_up_down(self, up):
        old_datas = copy.deepcopy(self.data)
        for col in range(COLS):
            valid_data = [self.data[row][col] for row in range(ROWS) if self.data[row][col] != 0]
            if len(valid_data) >= 2:
                score = self.update(valid_data, up)
                if score > self.cur_score:
                    self.cur_score = score
            for i in range(ROWS - len(valid_data)):
                if up:
                    valid_data.append(0)
                else:
                    valid_data.insert(0, 0)
            for row in range(ROWS):
                self.data[row][col] = valid_data[row]
        return old_datas != self.data

    def move_left_right(self, left):
        old_data = copy.deepcopy(self.data)
        for row in range(ROWS):
            valid_data = [self.data[row][col] for col in range(COLS) if self.data[row][col] != 0]
            if len(valid_data) >= 2:
                score = self.update(valid_data, left)
                if score > self.cur_score:
                    self.cur_score = score
            for i in range(COLS - len(valid_data)):
                if left:
                    valid_data.append(0)
                else:
                    valid_data.insert(0, 0)
            for col in range(COLS):
                self.data[row][col] = valid_data[col]
        return old_data != self.data

    def do_move(self, move):
        if move:
            self.is_new_record()
            self.next_step()
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
            self.draw_data(dc)
            self.draw_score(dc)
            self.is_game_over()

    # 若打破最高分的纪录，存储新的纪录
    def is_new_record(self):
        if self.cur_score > self.high_score:
            self.high_score = self.cur_score
            self.save_record()
            # wx.MessageDialog(None, u"新纪录 " + str(self.high_score), style=wx.OK or wx.ICON_INFORMATION)

    # 判断游戏结束
    def is_game_over(self):
        copy_data = copy.deepcopy(self.data)
        if not self.move_left_right(True) and not self.move_left_right(False) \
                and not self.move_up_down(True) and not self.move_up_down(False):
            dlg = wx.MessageDialog(None, u"游戏结束，再来一局？", style=wx.YES_NO or wx.YES_DEFAULT or wx.ICON_QUESTION)
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                self.init_game()
            elif result == wx.ID_NO:
                self.on_exit_game()
            dlg.Destroy()
        else:
            self.data = copy_data


class Frame(wx.Frame):
    def __init__(self, title):
        super(Frame, self).__init__(None, -1, title, style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^
                                                           wx.RESIZE_BORDER)
        self.SetIcon(wx.Icon('icon.jpg'))
        self.set_menu()
        self.window = MainWindow(self)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    # 设置菜单栏
    def set_menu(self):
        # 创建菜单栏及菜单,并绑定监听器
        file_menu_bar = wx.MenuBar()
        self.SetMenuBar(file_menu_bar)
        file_menu = wx.Menu()
        file_menu_bar.Append(file_menu, u"surprise")

        menu_save_game = file_menu.Append(wx.ID_SAVE, "存档")
        file_menu.AppendSeparator()
        menu_load_game = file_menu.Append(wx.ID_OPEN, "读档")
        file_menu.AppendSeparator()
        file_menu.Append(wx.ID_SETUP, u"重新开始")

        self.Bind(wx.EVT_MENU, self.handle_menu)

    def handle_menu(self, event):
        id = event.GetId()
        if id == wx.ID_SAVE:
            self.on_save_game(event)
        if id == wx.ID_OPEN:
            self.on_load_game(event)
        if id == wx.ID_SETUP:
            self.window.init_game()

    # 游戏存档
    def on_save_game(self, event):
        data_str = ''
        for i in range(ROWS):
            for j in range(COLS):
                data_str += (str(self.window.data[i][j]) + '.')
        with open('gamefile.ini', 'w', encoding='utf-8')as fw:
            fw.write(data_str)

    # 游戏读档
    def on_load_game(self, event):
        if os.path.exists('gamefile.ini'):
            with open('gamefile.ini', 'r', encoding='utf-8')as fr:
                data_str = fr.read()
            data_list = data_str.split('.')
            for i in range(ROWS):
                for j in range(COLS):
                    self.window.data[i][j] = int(data_list[i * 4 + j])
            self.window.draw_all()
        else:
            wx.MessageDialog(self, u"没有存档", u"提示", style=wx.OK)

    def on_close(self, event):
        self.on_save_game(event)
        self.Destroy()


class APP(wx.App):
    def on_init(self):
        self.frame = Frame(title=u"2048 v1.0 by hb")
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
