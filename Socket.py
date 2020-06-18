#!/usr/bin/env python3
__author__ = "Copyright ⓒ 2020 by www.chenxuanwei.com"
### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
### Socket类封装
### Version 2.0
### 2020-06-17
### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
import socket as SOCKET
import time, sys, threading
class Debug:

    @staticmethod
    def output(str):
        print(str)

class Socket:

    description = "socket class的重定义封装"
    
    sessions = 10
    host = "localhost"
    port = 8080
    INTERVAL = 5

    #### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ####
    #### messages defination between MAC and RaspberryPi
    msgHandshake = "Welcome to my server"
    msgGPIO_ON   = "GPIO_ON"
    msgGPIO_OFF  = "GPIO_OFF"

    def __init__(self, host = "localhost", port = 8080, callback = None): 
        self.host     = host
        self.port     = port
        self.callback = callback
        self.server   = None

    def send(self, sock, text):   
        sock.send(str.encode(text))
    
    def recv(self, sock): 
        data = sock.recv(1024)
        return (bytes.decode(data))

    #### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ####
    #### 启动服务器端程序
    #### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ####
    def runServer(self):
        loop = 0
        interval = 5
        while not self.initSocket(side = "server"):
            time.sleep(interval)
            loop += interval
            Debug.output("{} seconds passed!".format(loop))

        Debug.output("Socket successfully initialed.Now it is starting ...")
        index = 0
        while True:  #循环轮询socket状态，等待访问
                
                client, address = self.server.accept()
                Debug.output("\n\nclient = {}, address = {}\n".format(client, address))
                index = (index + 1) % 1000
                

                self.send(sock = client, text = self.msgHandshake)
                #当获取一个新连接时，启动一个新线程来处理这个连接
                threading.Thread(target = self.children, args = (index, self.server, client,)).start()
        sock.close()

    #### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ####
    #### 服务器端启动的子线程处理每一个客户端的数据请求。
    #### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ####
    def children(self, index, server, client):
        Debug.output("\n\n子线程No.{} 启动。。。\n".format(index))
        while True:
            data = self.recv(sock = client)
            Debug.output("\n从{}获取数据: {}\n".format(client, data))

            data = self.cmdApproach(data)
            
            if data == "exit":
                Debug.output("Child No.{} is closing.".format(index))
                self.send(sock = client, text = data)
                client.close()
                return
            else:
                self.send(sock = client, text = data)
            

    def cmdApproach(self, cmd):
        Debug.output("🟡🟡🟡🟡🟡: " + cmd)
        if cmd == self.msgGPIO_ON: 

            return self.msgGPIO_ON

        elif cmd == self.msgGPIO_OFF:

            return self.msgGPIO_OFF

        else:
            return cmd


    #### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ####
    #### 初始化和关闭客户端
    #### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ####
    def initClient(self):
        loop = 0
        interval = 5
        while not self.initSocket(side = "client"):
            time.sleep(interval)
            loop += interval
            Debug.output("{} seconds passed!".format(loop))

        Debug.output("Socket successfully initialed. \n\nNow it is starting ...")
    def closeClient(self):
        Debug.output("send the exit to server")
        self.send2Server(data = "exit")


    #### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ####
    #### 初始化客户端或者服务器端的Socket
    #### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ####
    def initSocket(self, side):
        try:
            self.server = SOCKET.socket(SOCKET.AF_INET, SOCKET.SOCK_STREAM)
            if side == "server":
                self.server.bind((self.host, self.port))  #配置soket，绑定IP地址和端口号
                self.server.listen(5) #设置最大允许连接数，各连接和server的通信遵循FIFO原则
            else:
                self.server.connect((SOCKET.gethostbyname(self.host), self.port))
                data = self.recv(sock = self.server)
                Debug.output(data)
                if self.callback:   self.callback(cmd = data)
            return True
        except OSError:
            Debug.output("Socket初始化失败！")
            return False




    #### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ####
    #### 客户端发送数据到客户端，并接受从服务端的返回数据
    #### 🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴🔴 ####
    def send2Server(self, data):
        self.send(sock = self.server, text = data)
        data = self.recv(sock = self.server)
        Debug.output("Get confirm from server: {}".format(data))
        if self.callback:
            self.callback(data)
        
        if data == "exit":
            Debug.output("Closing connection!")
            self.server.close()
            return;       

#### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
####  Entry of the Server and Test program.  
if __name__ == "__main__": 
    help = "\n\nUsage: {} [server/client]\n\n d".format(sys.argv[0])

    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "server"):

        Socket().runServer()

    elif len(sys.argv) == 2 and sys.argv[1] == "client":
        sock = Socket()
        sock.initClient()
        Debug.output("\n\n初始化完成。。。。\n\n")
        sock.send2Server(data = "run")

    else:
        Debug.output(help)
### 🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅🍅 ###
