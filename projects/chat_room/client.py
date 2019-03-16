# -*- coding:utf-8 -*-
import wx
import telnetlib
from time import sleep
import _thread as thread


class LoginFrame(wx.Frame):
    """
    the login window
    """

    def __init__(self, parent, id, title='', size=wx.DefaultSize):
        # initialize,bind the buttons with the control methods
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.server_addressLabel = wx.StaticText(self, label="Server Address", pos=(10, 50), size=(120, 25))
        self.userNameLabel = wx.StaticText(self, label="UserName", pos=(40, 100), size=(120, 25))
        self.server_address = wx.TextCtrl(self, pos=(120, 47), size=(150, 25))
        self.userName = wx.TextCtrl(self, pos=(120, 97), size=(150, 25))
        self.loginButton = wx.Button(self, label="Login", pos=(80, 145), size=(130, 30))
        # 绑定登录方法
        self.loginButton.Bind(wx.EVT_BUTTON, self.login)
        self.Show()

    def check_address(self):
        #   check the server address
        flag = False
        server_address = self.server_address.GetLineText(0)
        if server_address == '':
            self.show_dialog('Error', 'ServerAddress Empty!', (200, 100))
        else:
            server_address = self.server_address.GetLineText(0).split(':')
            if 2 > len(server_address):
                self.show_dialog('Error', 'ServerAddress Error!', (200, 100))
            else:
                if 4 > len(server_address[0].split('.')):
                    self.show_dialog('Error', 'ServerAddress Error', (200, 100))
                else:
                    flag = True
        return flag

    def login(self, event):
        # login
        # try:
        # server_address = self.server_address.GetLineText(0)
        # if server_address == '':
        #     self.show_dialog('Error', 'ServerAddress Empty!', (200, 100))
        # else:
        #     server_address = self.server_address.GetLineText(0).split(':')
        #     if 2 > len(server_address):
        #         self.show_dialog('Error', 'ServerAddress Error!', (200, 100))
        #     else:
        #         if 3 > len(server_address[0].split('.')) :
        #             self.show_dialog('Error','ServerAddress Error',(200,100))
        #         else:
        if self.check_address():
            server_address = self.server_address.GetLineText(0).split(':')
            con.open(server_address[0], port=int(server_address[1]), timeout=10)
            response = con.read_some()
            if response != b'Connect Success':
                self.show_dialog('Error', 'Connect Fail', (200, 100))
                return
            con.write(('login ' + str(self.userName.GetLineText(0)) + '\n').encode("utf-8"))
            response = con.read_some()
            if response == b'UserName Empty':
                self.show_dialog('Error', 'UserName Empty!', (200, 100))
            elif response == b'UserName Exist':
                self.show_dialog('Error', 'UserName Exist!', (200, 100))
            else:
                self.Close()
                ChatFrame(None, 2, title='Chat Client', size=(500, 400))
                # except Exception:
                #     self.show_dialog('Error', 'Connect Fail!', (200, 100))

    def show_dialog(self, title, content, size):
        # 显示错误信息对话框
        dialog = wx.Dialog(self, title=title, size=size)
        dialog.Center()
        wx.StaticText(dialog, label=content)
        dialog.ShowModal()


class ChatFrame(wx.Frame):
    """
    the chat window
    """

    def __int__(self, parent, id, title, size):
        # initializing,add controls and bind events
        wx.Frame.__init__(self, parent, id, title)
        self.SetSize(size)
        self.Center()
        self.chatFrame = wx.TextCtrl(self, pos=(5, 5), size=(490, 310), style=wx.TE_READONLY)
        self.message = wx.TextCtrl(self, pos=(5, 320), size=(300, 25))
        self.sendButton = wx.Button(self, label="Send", pos=(310, 320), size=(58, 25))
        self.userButton = wx.Button(self, label="Users", pos=(373, 320), size=(58, 25))
        self.closeButton = wx.Button(self, label="Close", pos=(436, 320), size=(58, 25))
        # bind the buttons with the control methods
        self.sendButton.Bind(wx.EVT_BUTTON, self.send)
        self.userButton.Bind(wx.EVT_BUTTON, self.look_users)
        self.closeButton.Bind(wx.EVT_BUTTON, self.close)
        thread.start_new_thread(self.receive, ())
        self.Show()

    def send(self, event):
        # send the message
        message = str(self.message.GetLineText(0).strip())
        if message != '':
            con.write(('say ' + message + '\n').encode('utf-8'))
            self.message.Clear()

    def look_users(self, event):
        # look the online users
        con.write(b'look\n')

    def receive(self):
        # receive the message from server
        while True:
            sleep(0.6)
            result = con.read_very_eager()
            if result != '':
                self.chatFrame.AppendText(result)


if __name__ == '__main__':
    app = wx.App()
    con = telnetlib.Telnet()
    LoginFrame(None, -1, title="Login", size=(320, 240))
    app.MainLoop()
