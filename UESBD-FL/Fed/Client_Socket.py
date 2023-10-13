#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/4/22 15:36
import hashlib
import os
import socket
import json

import torch
import sys

sys.setrecursionlimit(1000000)

ADDRESS = ('127.0.0.1', 8182)
# ADDRESS = ('192.168.0.199',c 8183)
client_type = 'xnhyacinth'


class client_socket():
    def __init__(self):
        self.conn = socket.socket()
        self.conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
        self.conn.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
        self.conn.connect(ADDRESS)
        self.client_type = client_type

        # self.input_client_type()

    def send_data(self, conn, cmd, data, **kv):
        jd = {}
        jd['COMMAND'] = cmd
        jd['client_type'] = self.client_type
        jd['data'] = data
        jd['index'] = kv

        jsonstr = json.dumps(jd)
        print('send: ' + jsonstr)
        conn.sendall(jsonstr.encode('utf8'))
        if cmd == "send_model":
            self.send_local_model(data)

    def input_client_type(self):
        self.client_type = input("注册客户端，请输入名字:")

    def receive_data(self, data):
        server_response = self.conn.recv(1024).decode("utf-8")

        # 1.先接收长度，建议8192
        file_size = int(server_response)

        print("接收到的大小：", file_size)

        # 2.接收文件内容
        self.conn.send("准备好接收".encode("utf-8"))  # 接收确认
        filename = "new" + data + "{}".format(self.client_type)

        f = open(filename, "wb")
        received_size = 0
        m = hashlib.md5()

        while received_size < file_size:
            size = 0  # 准确接收数据大小，解决粘包
            if file_size - received_size > 1024:  # 多次接收
                size = 1024
            else:  # 最后一次接收完毕
                size = file_size - received_size

            data = self.conn.recv(size)  # 多次接收内容，接收大数据
            data_len = len(data)
            received_size += data_len
            # print("已接收：", int(received_size / file_size * 100), "%")

            m.update(data)
            f.write(data)

        f.close()

        print("实际接收的大小:", received_size)  # 解码

        # 3.md5值校验
        md5_sever = self.conn.recv(1024).decode("utf-8")
        md5_client = m.hexdigest()
        print("服务器发来的md5:", md5_sever)
        print("接收文件的md5:", md5_client)
        if md5_sever == md5_client:
            print("MD5值校验成功")
        else:
            print("MD5值校验失败")

        return torch.load(filename)

    def send_local_model(self, model):
        # 1.先发送文件大小，让客户端准备接收
        size = os.stat(model).st_size  # 获取文件大小
        self.conn.send(str(size).encode("utf-8"))  # 发送数据长度
        print("发送的大小：", size)

        # 2.发送文件内容
        self.conn.recv(1024)  # 接收确认

        m = hashlib.md5()
        f = open(model, "rb")
        for line in f:
            self.conn.send(line)  # 发送数据
            m.update(line)
        f.close()

        # 3.发送md5值进行校验
        md5 = m.hexdigest()
        self.conn.send(md5.encode("utf-8"))  # 发送md5值
        print("md5:", md5)


if '__main__' == __name__:
    c = client_socket()

    # print(client.recv(1024).decode(encoding='utf8'))

    while True:
        a = input("请输入要发送的信息:")
        c.send_data(c.conn, 'SEND_DATA', data=a)
