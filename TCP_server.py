import socket
import threading


# 指定本地端口
IP = '127.0.0.1'
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPV4， TCP服务
    server.bind((IP, PORT))
    server.listen(5)  # 指定最大连接数量
    print(f'[*] 当前监听: {IP}:{PORT}')

    while True:
        client, address = server.accept()  # 将接收到的客户端socket对象保存到client变量中，远程连接信息传入adress当中
        print(f'[*] 接收连接来自：{address[0]}:{address[1]}')
        # 创建一个新的线程，指向handler_client函数，并传入client对象,
        # 需要在变量 client 之后添加一个逗号。只发送 client toargs= ()是尝试解包多个参数，而不是只发送一个参数
        client_handler = threading.Thread(target=handler_client, args=(client,)) 
        print('[*] 线程已启动')
        client_handler.start()  # 启动该线程

def handler_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)  # 接收数据
        print(f'[*] 已接收: {request.decode("utf-8")}')
        sock.send(b'ACK')

if __name__ == "__main__":
    main()

