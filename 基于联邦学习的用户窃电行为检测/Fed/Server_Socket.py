#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/4/22 15:36

import hashlib
import json
import os
import socket  # 导入 socket 模块
import threading
from threading import Thread
import time
from evaluate import evaluate_fn
from metrics import metrics_report
from torch.utils.data import DataLoader
from Hybrid_Attn import HybridAttentionModel
from dataset import FraudDataset
from data import *

sys.setrecursionlimit(1000000)

ADDRESS = ('127.0.0.1', 8182)  # 绑定地址

g_socket_server = None  # 负责监听的socket


class Server(object):
    def __init__(self, num, num_comm, dev):
        self.g_conn_pool = {}  # 连接池
        self.sum_parameters = {}
        self.global_parameters = {}
        self.sum_client = 0
        self.id = 0
        self.flag = 0  # 结束判断
        self.send = 0  # 发送判断
        self.valid_loader = None
        self.clients_num = num
        self.num_comm = num_comm
        self.net = HybridAttentionModel()
        self.params = []  # 参数
        self.losses = []  # 损失
        self.length = []  # 样本数
        self.clients = []  # 客户端
        self.scores = []  # 贡献度
        self.criterion = torch.nn.CrossEntropyLoss()
        self.valid_losses = []
        self.f1s = []
        self.best_f1 = -1
        self.best_com = -1
        self.dev = dev
        """
        初始化服务端
        """
        global g_socket_server
        g_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        g_socket_server.bind(ADDRESS)
        g_socket_server.listen(5)  # 最大等待数（有很多人理解为最大连接数，其实是错误的）
        print("server start，wait for client connecting...")
        self.load_eval_data()

    def load_eval_data(self):
        # 读取验证集
        X_eval, y_eval = GetDataSet('data/eval.csv')
        dataset_eval = FraudDataset(X_eval, y_eval)

        self.valid_loader = DataLoader(dataset=dataset_eval, batch_size=100, shuffle=False)

    def accept_client(self):
        """
        接收新连接
        """
        while True:
            client, info = g_socket_server.accept()  # 阻塞，等待客户端连接
            client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
            client.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 60 * 1000, 30 * 1000))
            # 给每个客户端创建一个独立的线程进行管理
            thread = Thread(target=self.message_handle, args=(client, info))
            # 设置成守护线程
            thread.setDaemon(True)
            thread.start()

    def message_handle(self, client, info):
        """
        消息处理
        """
        client.sendall("connect server successfully!".encode(encoding='utf8'))
        while True:
            try:
                mutex = threading.Lock()
                mutex.acquire()
                bytes = client.recv(1024)
                msg = bytes.decode(encoding='utf8')
                jd = json.loads(msg)
                cmd = jd['COMMAND']
                client_type = jd['client_type']
                if 'CONNECT' == cmd:
                    self.g_conn_pool[client_type] = client
                    print('on client connect: ' + client_type, info)
                elif 'SEND_DATA' == cmd:
                    print('recv client msg: ' + client_type, jd['data'])
                elif 'get' == cmd:
                    filename = jd['data']
                    self.send_model(client, filename)
                elif 'send_model' == cmd:
                    self.id = jd['index']['index']
                    self.receive_local_model(client, jd['data'] + "_" + client_type)
                    local_parameters = {}
                    self.sum_client += 1
                    self.length.append(jd['index']['length'])
                    self.clients.append(client_type)
                    self.losses.append(jd['index']['loss'])
                    self.params.append(copy.deepcopy(self.net.state_dict()))
                    for key, var in self.net.state_dict().items():
                        # print("key:"+str(key)+",var:"+str(var))
                        # print("张量的维度:" + str(var.shape))
                        # print("张量的Size" + str(var.size()))
                        local_parameters[key] = var.clone()
                    # print(local_parameters)
                    if len(self.sum_parameters) == 0:
                        for key, var in local_parameters.items():
                            self.sum_parameters[key] = var.clone()
                        self.global_parameters = self.sum_parameters
                    else:
                        for var in self.sum_parameters:
                            self.sum_parameters[var] = self.sum_parameters[var] + local_parameters[var]

                if self.sum_client == self.clients_num:
                    # 取平均值，得到本次通信中Server得到的更新后的模型参数
                    # for var in self.global_parameters:
                    #     self.global_parameters[var] = (self.sum_parameters[var] / self.sum_client)
                    # print(self.global_parameters)
                    print(1)
                    self.global_parameters = FedAvg_LA(self.params, self.losses)
                    self.net.load_state_dict(copy.deepcopy(self.global_parameters), strict=True)
                    self.net.to(self.dev)
                    torch.save(self.net, "global_model_%d" % (self.id + 1))

                    # cal contribution
                    contributions = cal_contribution(self.losses, self.scores, self.id, self.clients)

                    # model eval
                    self.eval_model(self.net, self.valid_loader, self.criterion, self.best_f1, device=self.dev,
                                    verbose=True)
                    # 结束通讯
                    if self.id + 1 == self.num_comm:
                        self.flag = 1
                        # 记录贡献值
                        for c in self.clients:
                            jd = {}
                            jd = {'client': c, 'contribution': "{:.4}".format(contributions[c] * 100)}
                            jd = json.dumps(jd, ensure_ascii=False)
                            with open(os.path.join("./", 'log/log_{}.json'.format(c)), 'a') as f:
                                f.write(jd + '\n')
                                f.close()
                        break
                    self.send = 1

                mutex.release()

            except Exception as e:
                print(e)
                self.remove_client(client_type)
                break

    def eval_model(self, model, eval_loader, criterion, best_f1, device='cpu', verbose=False):
        valid_loss, tn, fp, fn, tp, precision, recall, f1Score = evaluate_fn(model, eval_loader, criterion,
                                                                             device, verbose=verbose)
        self.valid_losses.append(valid_loss)
        self.f1s.append(f1Score)
        if f1Score > best_f1:
            self.best_f1 = f1Score
            self.best_com = self.id + 1
        if verbose:
            jd = {}
            jd['communicate_index'] = self.id + 1
            jd['valid_loss'] = "{:.3}".format(valid_loss)
            jd['tn'] = "{}".format(tn)
            jd['fp'] = "{}".format(fp)
            jd['fn'] = "{}".format(fn)
            jd['tp'] = "{}".format(tp)
            jd['accuracy'] = "{:.3}".format((tn + tp) / (tn + tp + fn + fp))
            jd['precision'] = "{:.3}".format(precision)
            jd['recall'] = "{:.3}".format(recall)
            jd['f1Score'] = "{:.3}".format(f1Score)

            metrics_report(model, eval_loader, jd, name="server", device=device)

    def remove_client(self, client_type):
        client = self.g_conn_pool[client_type]
        if None != client:
            client.close()
            self.g_conn_pool.pop(client_type)
            print("client offline: " + client_type)

    def send_model(self, conn, model):
        if os.path.isfile(model):  # 判断文件存在
            # 1.先发送文件大小，让客户端准备接收
            size = os.stat(model).st_size  # 获取文件大小
            conn.send(str(size).encode("utf-8"))  # 发送数据长度
            print("发送的大小：", size)

            # 2.发送文件内容
            conn.recv(1024)  # 接收确认

            m = hashlib.md5()
            f = open(model, "rb")
            for line in f:
                conn.send(line)  # 发送数据
                m.update(line)
            f.close()

            # 3.发送md5值进行校验
            md5 = m.hexdigest()
            conn.send(md5.encode("utf-8"))  # 发送md5值
            print("md5:", md5)
        else:
            conn.send("wait".encode("utf-8"))
            self.send_model(conn, model)

    def receive_local_model(self, conn, data):

        # 1.先接收长度，建议8192
        server_response = conn.recv(1024)
        file_size = int(server_response.decode("utf-8"))

        print("接收到的大小：", file_size)

        # 2.接收文件内容
        conn.send("准备好接收".encode("utf-8"))  # 接收确认
        filename = data

        f = open(filename, "wb")
        received_size = 0
        m = hashlib.md5()

        while received_size < file_size:
            size = 0  # 准确接收数据大小，解决粘包
            if file_size - received_size > 1024:  # 多次接收
                size = 1024
            else:  # 最后一次接收完毕
                size = file_size - received_size

            data = conn.recv(size)  # 多次接收内容，接收大数据
            data_len = len(data)
            received_size += data_len
            # print("已接收：", int(received_size / file_size * 100), "%")

            m.update(data)
            f.write(data)

        f.close()

        print("实际接收的大小:", received_size)  # 解码

        # 3.md5值校验
        md5_sever = conn.recv(1024).decode("utf-8")
        md5_client = m.hexdigest()
        print("服务器发来的md5:", md5_sever)
        print("接收文件的md5:", md5_client)
        if md5_sever == md5_client:
            print("MD5值校验成功")
        else:
            print("MD5值校验失败")
        self.net.load_state_dict(torch.load(filename))

# if __name__ == '__main__':
#     server = Server()
#     # init()
#     # 新开一个线程，用于接收新连接
#     thread = Thread(target=server.accept_client)
#     thread.setDaemon(True)
#     thread.start()
#     # 主线程逻辑
#     server.eval_model(server.net, server.valid_loader, server.criterion, server.valid_losses, server.f1s,
#                       server.best_f1, server.best_com, verbose=True)
