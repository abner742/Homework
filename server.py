from http.server import BaseHTTPRequestHandler,HTTPServer
import os,sys
import subprocess
class ServerException(Exception):
    """服务器内部错误"""
    pass

#case的基类
class case_base(object):
    def handle_file(self,handler):
        try:
            with open(handler.full_path,'rb') as reader:
                content=reader.read()
            handler.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read: {1}".format(handler.full_path, msg)
            handler.handle_error(msg)

    def test(self, handler):
        assert False,"Not Impletment"

    def act(self, handler):
        assert False,"Not Impletment"

    def index_file(self,handler):
        return os.path.join(handler.full_path,"index.html")

# 不存在该路径
class no_path(case_base):
    def test(self,handler):
        return not os.path.exists(handler.full_path)
    def act(self,handler):
        raise Exception("{0} not found".format(handler.path))
#该路径是一个文件
class is_file(case_base):
    def test(self,handler):
        return os.path.isfile(handler.full_path)
    def act(self,handler):
        self.handle_file(handler)
#该路径不是一个文件
class not_file(case_base):
    def test(self,handler):
        return True
    def act(self,handler):
        raise Exception("{0} unknown object".format(handler.path))
#浏览器访问根url的时候能返回工作目录下index.html的内容
class index_file(case_base):
    def index_path(self,handler):
        return os.path.join(handler.full_path,'index.html')
    def test(self,handler):
        return os.path.isdir(handler.full_path) and \
                os.path.isfile(self.index_path(handler))
    def act(self,handler):
        return self.handle_file(handler)
#利用cgi协议处理外部文件
class cgi_file(case_base):
    def test(self,handler):
        return os.path.isfile(handler.full_path) and \
                handler.full_path.endswith(".py")
    def act(self,handler):
        self.run_cgi(handler)
    def run_cgi(self,handler):
        data = subprocess.check_output(["python",handler.full_path],shell=False)
        print(data)
        handler.send_content(data)

class RequestHandler(BaseHTTPRequestHandler):
    cases = [no_path(),cgi_file(),is_file(),index_file(),not_file()]
    #一定要注意这个顺序，cgi_file和is_file条件是包含关系，一定要将cgi放前面
    def do_GET(self):
        try:
            self.full_path =os.getcwd()+self.path
            for case in self.cases:
                if(case.test(self)):
                    case.act(self)
                    break
        #处理异常
        except Exception as msg:
            self.handle_error(msg)#因为这里使用了handle_error所以它要写到这个类里面
    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """
    def handle_error(self,msg):
        content=self.Error_Page.format(path=self.path,msg=msg)
        self.send_content(content.encode('utf-8'),404)

    def send_content(self, page,status=200):
        self.send_response(status)
        self.send_header("Content-Type","text/html")
        self.send_header("Content-Length",str(len(page)))
        self.end_headers()
        self.wfile.write(page)

if __name__ == "__main__":
    serverAddress=('',8089)
    server=HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()