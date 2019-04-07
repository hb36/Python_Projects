import wx


class Frame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)

        self.panel = wx.Panel(self, -1, style=wx.BORDER_NONE)
        self.panel.Bind(wx.EVT_KEY_DOWN, self.key_down)
        self.Bind(wx.EVT_KEY_DOWN, self.key_down)
        # self.panel.SetFocus()
        self.Centre()
        # self.btn = wx.Button(self, -1, u"按一下看看", pos=(0, 0), size=(80, 60))
        # self.Bind(wx.EVT_KEY_DOWN,self.key_down,self.btn)

        data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.colours = {0: (255, 235, 225)}
        for i in range(1, 17):
            self.colours[2 ** i] = (
                255, 235 - 13 * i if 235 - 13 * i > 0 else 0, 225 - 19 * i if 225 - 19 * i > 0 else 0)
        self.data_show = [[], [], [], []]
        self.num = 1
        for i in range(4):
            for j in range(4):
                self.data_show[i].append(
                    wx.Button(self.panel, -1, label=str(2 ** self.num), pos=(100 + 100 * i, 100 + 70 * j),
                              size=(100, 70)))
                self.num += 1
        self.count = 1
        for i in range(4):
            for j in range(4):
                self.data_show[i][j].SetBackgroundColour(self.colours[2 ** self.count])
                self.count += 1

        # self.data_show[0][3].Bind(wx.EVT_KEY_DOWN,self.key_down)
        self.Show(True)

    def key_down(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_UP:
            self.SetTitle(chr(key_code))

            self.data_show[0][3].SetBackgroundColour((200, 30, 123))
            self.data_show[0][3].SetLabel("success")
        elif key_code == 83:
            self.data_show[3][3].SetBackgroundColour((30, 200, 88))
            self.data_show[3][3].SetLabel("123456")
            # self.btn.SetLabel(u"啥玩意")


def main():
    app = wx.App()
    Frame(None, -1, "A test on keydown event")
    app.MainLoop()


if __name__ == '__main__':
    main()
