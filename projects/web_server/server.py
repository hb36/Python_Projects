# encoding:utf-8
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import sys
import subprocess


class ServerException(Exception):
    '''服务器内部错误'''
    pass


class BaseCase(object):
    def handle_file(self, handler, full_path):
        try:
            with open(full_path, 'rb')as fr:
                content = fr.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(full_path, msg)
            handler.handle_error(msg)

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        assert False, 'Not implemented.'

    def act(self, handler):
        assert False, 'Not implemented.'


class CaseNoFile(BaseCase):
    '''文件或目录不存在'''

    def test(self, handler):
        return not os.path.exists(handler.full_path)

    def act(self, handler):
        raise ServerException("'{0}' not found".format(handler.path))


class CaseCgiFile(BaseCase):
    '''可执行脚本'''

    def run_cgi(self, handler):
        data = subprocess.check_output(["python", handler.full_path], shell=False)
        handler.send_content(data)

    def test(self, handler):
        return os.path.isfile(handler.full_path) and handler.full_path.endswith('.py')

    def act(self, handler):
        self.run_cgi(handler)


class CaseExistingFile(BaseCase):
    '''文件存在'''

    def test(self, handler):
        return os.path.isfile(handler.full_path)

    def act(self, handler):
        self.handle_file(handler, handler.full_path)


class CaseFail(BaseCase):
    '''默认处理'''

    def test(self, handler):
        return True

    def act(self, handler):
        raise ServerException("Unkonwn object '{0}'".format(handler.path))


class CaseDirectoryIndexFile(BaseCase):
    '''在根路径下返回主页文件'''

    def index_path(self, handler):
        return os.path.join(handler.full_path, 'index.html')

    def test(self, handler):
        return os.path.isdir(handler.full_path) and os.path.isfile(self.index_path((handler)))

    def act(self, handler):
        self.handle_file(handler, self.index_path(handler))


class RequestHandler(BaseHTTPRequestHandler):
    '''
    请求路径合法则返回相应处理
    否则返回错误页面
    '''
    Cases = [CaseNoFile(),
             CaseCgiFile(),  # 先判断是否脚本文件，再判断是否普通文件
             CaseExistingFile(),
             CaseDirectoryIndexFile(),
             CaseFail()]
    Error_Page = '''
    <html>
    <body>
    <h1>Error accessing {path}</h1>
    <p>{msg}</p>
    </body>
    </html>
    '''

    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path
            for case in self.Cases:
                if case.test(self):
                    case.act(self)
                    break
        except Exception as msg:
            self.handle_error(msg)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content.encode('utf-8'), 404)

    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == '__main__':
    server_address = ('', 8080)
    server = HTTPServer(server_address, RequestHandler)
    server.serve_forever()
