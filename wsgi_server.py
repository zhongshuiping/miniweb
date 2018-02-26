import socket
import re
from threading import Thread
import gevent


class HTTPServer(object):

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', 8888))
        self.server.listen(10)

    def start(self):
        while True:
            self.client, self.address = self.server.accept()
            g1 = gevent.spawn(self.handRequest())
            g1.join()
            # th = Thread(target=self.handRequest)
            # th.start()

    def handRequest(self):
        while True:
            print('用户%s来了' % str(self.address))
            data = self.client.recv(2048)
            data_list = data.decode('utf-8').split('\r\n')

            data_header = data_list[0]
            file_name = re.search(r'\s(/.*)\s',data_header).group().strip()
            if file_name == '/':
                file_name = '/index.html'
            try:
                file = open('./static'+file_name,'rb')
            except FileNotFoundError as e:
                responseLine = 'HTTP 404 Not Found \r\n'
                responseHeader = 'Server: PM1.0 \r\n'
                responseHeader += 'Content-Type:text/html\r\n'
                content = 'error file'
                response = (responseLine + responseHeader + '\r\n' + content).encode('utf-8')

            else:
                content = file.read()
                responseLine = 'HTTP 200 OK \r\n'
                responseHeader = 'Server: PM1.0 \r\n'
                responseHeader += 'Content-Type:text/html\r\n'
                response = (responseLine + responseHeader + '\r\n').encode('utf-8') + content
            finally:
                self.client.send(response)
                self.client.close()
                break

def main():

    http = HTTPServer()
    http.start()

if __name__ == '__main__':
    main()