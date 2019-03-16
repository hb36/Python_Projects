# -*- coding:utf-8 -*-
import asyncore
import asynchat

PORT = 8080  # 定义端口
HOST = '127.0.0.1'


class EndSession(Exception):  # 定义结束异常类
    pass


class ChatServer(asyncore.dispatcher):
    """
    聊天服务器
    """

    def __init__(self, port):
        asyncore.dispatcher.__init__(self)
        # 创建socket
        self.create_socket()
        # 设置socket为可重用
        self.set_reuse_addr()
        # 监听端口
        self.bind((HOST, port))
        self.listen(5)
        self.users = {}
        self.main_room = ChatRoom(self)

    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)


class ChatSession(asynchat.async_chat):
    """
    负责和客户端通信
    """

    def __init__(self, server, sock):
        asynchat.async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator(b'\n')
        self.data = []
        self.name = None
        self.enter(LoginRoom(server))

    def enter(self, room):
        # 从当前房间移除自身，然后添加到指定房间
        try:
            room_current = self.room
        except AttributeError:
            pass
        else:
            room_current.remove(self)
        self.room = room
        room.add(self)

    def cellect_income_data(self, data):
        # 接收客户端的数据
        self.data.append(data.decode("utf-8"))

    def found_terminator(self):
        # 当客户端的一条数据结束时的处理
        line = ''.join(self.data)
        self.data = []
        try:
            self.room.handle(self, line.encode("utf-8"))
        # 退出聊天室的处理
        except EndSession:
            self.handle_close()

    def handle_close(self):
        # 当session关闭时，将进入LogoutRoom
        asynchat.async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))


class CommandHandler:
    """
    命令处理类
    """

    def unknown(self, session, cmd):
        # 响应未知命令
        # 通过asynchat.async_chat.push方法发送消息
        session.push(('Unknown command {}\n'.format(cmd)).encode("utf-8"))

    def handle(self, session, line):
        line = line.decode()
        # 命令处理
        if not line.strip():
            return
        parts = line.split(' ', 1)
        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError:
            line = ' '
        # 通过协议代码执行相应的方法
        method = getattr(self, 'do_' + cmd, None)
        try:
            method(session, line)
        except TypeError:
            self.unknown(session, cmd)


class Room(CommandHandler):
    """
    包含多个用户的环境，负责基本的命令处理和广播
    """

    def __init__(self, server):
        self.server = server
        self.session = []

    def add(self, session):
        # 一个用户进入房间
        self.session.append(session)

    def remove(self, session):
        # 一个用户离开房间
        self.session.remove(session)

    def broadcast(self, line):
        # 向所有用户发送指令消息
        # 使用asynchat.asyn_chat.push 方法发送数据
        for session in self.session:
            session.push(line)

    def do_logout(self, session, line):
        # 退出房间
        raise EndSession


class LoginRoom(Room):
    """
    处理登录用户
    """

    def add(self, session):
        # 用户连接成功的回应
        Room.add(self, session)
        # 使用 asynchat.asyn_chat.push 方法发送数据
        session.push(b'Connect Success')

    def do_login(self, session, line):
        # 用户登录逻辑
        name = line.strip()
        # get user's name
        if not name:
            session.push(b'UserName Empty')
        # check if the username is used
        elif name in self.server.users:
            session.push(b'UserName Exist')
        # check out the username,go into the main_room
        else:
            session.name = name
            session.enter(self.server.main_room)


class LogoutRoom(Room):
    """
    处理退出用户
    """

    def add(self, session):
        # remove the user from the server
        try:
            del self.server.users[session.name]
        except KeyError:
            pass


class ChatRoom(Room):
    """
    the chat room
    """

    def add(self, session):
        # broadcasting the coming of the new user
        session.push(b'Login Success')
        self.broadcast((session.name + ' has entered the room.\n').encode('utf-8'))
        self.server.users[session.name] = session
        Room.add(self, session)

    def remove(self, session):
        #  broadcasting the leaving of the user
        Room.remove(self, session)
        self.broadcast((session.name + ' has left the room.\n').encode("utf-8"))

    def do_look(self, session, line):
        # the client sends the message
        self.broadcast((session.name + ':' + line + '\n').encode('utf-8'))


if __name__ == '__main__':
    s = ChatRoom(PORT)
    try:
        print("chat server runs at '{0}:{1}'".format(HOST, PORT))
        asyncore.loop()
    except KeyboardInterrupt:
        print("chat server exit")
