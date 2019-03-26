# encoding: utf-8
import wx
from math import *


class CalcFrame(wx.Frame):
    def __init__(self, title):
        super(CalcFrame, self).__init__(None, title=title, size=(400, 300))
        self.init_ui()
        self.Centre()
        self.Show()

    def init_ui(self):
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.textprint = wx.TextCtrl(self, style=wx.TE_RIGHT | wx.TE_READONLY)
        self.equation = ''
        self.textprint.SetValue(self.equation)
        vbox.Add(self.textprint, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)

        grid_box = wx.GridSizer(5, 4, 5, 5)
        labels = ['AC', 'DEL', 'pi', 'OFF', '7', '8', '9', '/', '4', '5', '6', '*',
                  '1', '2', '3', '-', '0', '.', '=', '+']

        for label in labels:
            button = wx.Button(self, label=label)
            self.create_handler(button, label)
            grid_box.Add(button, 0, wx.EXPAND)
        vbox.Add(grid_box, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)

    def create_handler(self, button, label):
        item = ['AC', 'DEL', 'OFF', '=']
        if label not in item:
            self.Bind(wx.EVT_BUTTON, self.on_calc, button)
        elif label == 'AC':
            self.Bind(wx.EVT_BUTTON, self.on_ac, button)
        elif label == 'DEL':
            self.Bind(wx.EVT_BUTTON, self.on_del, button)
        elif label == 'OFF':
            self.Bind(wx.EVT_BUTTON, self.on_exit, button)
        elif label == '=':
            self.Bind(wx.EVT_BUTTON, self.on_equal, button)

    def on_calc(self, event):
        event_btn = event.GetEventObject()
        label = event_btn.GetLabel()
        self.equation += label
        self.textprint.SetValue(self.equation)

    def on_ac(self, event):
        self.textprint.Clear()
        self.equation = ""

    def on_del(self, event):
        self.equation = self.equation[:-1]
        self.textprint.SetValue(self.equation)

    def on_exit(self, event):
        self.Close()

    def on_equal(self, event):
        string = self.equation
        try:
            result = eval(string)
            self.equation = str(result)
            self.textprint.SetValue(self.equation)
        except SyntaxError:
            dlg = wx.MessageDialog(self, u'格式错误，请输入正确的等式！',
                                   u'请注意', wx.OK | wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()


if __name__ == '__main__':
    app = wx.App()
    CalcFrame(title='Calculator')
    app.MainLoop()
