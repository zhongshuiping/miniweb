from multiprocessing import Process
import socket

def handle_client(client_socket):
    """处理客户端请求"""

    while True:
        data = client_socket.recv(1024)
        # 关闭客户端连接
        if data:
            print(data.decode('utf-8'))
        else:
            client_socket.close()
            print('连接已经断开')
            break

if __name__ == '__main__':
    # 创建tcp服务器
    tcp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    tcp_server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    tcp_server.bind(('',8080))
    tcp_server.listen(128)

    # 等待客户端的连接，并打印地址
    while True:
        client,address= tcp_server.accept()
        c = Process(target=handle_client,args=(client,))
        c.start()
        # 获取客户端请求数据
        reponseHeader = "HTTP/1.1 200 OK\r\n"
        responseMessage = "Server: My server\r\n"
        responseContent = "welcome to itcast"
        send_data = reponseHeader + responseMessage + responseContent
        client.send(send_data.encode('utf-8'))
        client.close()