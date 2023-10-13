#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/4/22 15:34

import time
from torch.utils.data import DataLoader, TensorDataset
from data import *
from torch import nn
from Client_Socket import *
import argparse
from dataset import FraudDataset
from evaluate import evaluate_fn
from metrics import metrics_report
import sys
from radam import RAdam

sys.setrecursionlimit(1000000)

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="FedAvg")
# 训练次数(客户端更新次数)
parser.add_argument('-E', '--epoch', type=int, default=1, help='local train epoch')
# batchsize大小
parser.add_argument('-B', '--batchsize', type=int, default=64, help='local train batch size')
parser.add_argument('-sp', '--save_path', type=str, default='./log', help='the saving path of checkpoints')


def test_mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


class Client(object):
    def __init__(self, name):
        self.name = name
        self.dev = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.train_loader = None
        self.local_parameters = None
        self.length = 0
        self.criterion = nn.CrossEntropyLoss()

        self.load_data()

    def train_one_epoch(self, model, dataloader, optim, criterion, device=torch.device("cpu")):
        loss_sum = 0
        model.to(device)
        model.train()
        print(4)
        for x, y in dataloader:
            output = model(x.to(device))
            loss = criterion(output, y.to(device))
            optim.zero_grad()
            loss.backward()
            optim.step()
            loss_sum += loss.item()
        print(6)
        return loss_sum / len(dataloader)

    def train(self, model, train_loader, criterion, index, output_dir='./', n_epochs=1, save_epochs=1,
              device=torch.device("cpu"),
              verbose=False):
        train_losses = []
        f1s = []
        best_f1 = -1
        best_epoch = 0
        optim = RAdam(model.parameters(), 0.001)
        for epoch in range(n_epochs):
            print(5)
            train_loss = self.train_one_epoch(model, train_loader, optim, criterion, device=device)
            print(7)
            # Accumulating train losses
            train_losses.append(train_loss)

            if epoch % save_epochs == 0:
                save_path = os.path.join(output_dir, 'local_model_{}_{}'.format(index, self.name))
                torch.save(copy.deepcopy(model.state_dict()), save_path)

            if verbose:
                jd = {}
                jd['communicate_index'] = index + 1
                jd['epoch'] = epoch + 1
                jd['train_loss'] = "{:.3}".format(train_loss)

                jd = json.dumps(jd)

                with open(os.path.join("./", 'log/log_{}.json'.format(self.name)), 'a') as f:
                    f.write(jd + '\n')
                    f.close()
                    print(3)

        return train_loss

    def load_data(self):
        X_train, y_train = GetDataSet('data/data_train_14000.csv')
        dataset_train = FraudDataset(X_train[:500], y_train[:500])
        self.length = len(dataset_train)
        self.train_loader = DataLoader(dataset=dataset_train, batch_size=100, shuffle=True)


if __name__ == "__main__":
    args = parser.parse_args()
    args = args.__dict__

    test_mkdir(args['save_path'])

    client_type = input("注册客户端，请输入名字:")
    client = Client(client_type)

    socket_c = client_socket()
    socket_c.client_type = client_type
    print(socket_c.conn.recv(1024).decode(encoding='utf8'))
    socket_c.send_data(socket_c.conn, 'CONNECT', '')
    flag = 0
    i = 0
    while True:
        # 获取全局模型
        socket_c.send_data(socket_c.conn, 'get', data="global_model_%d" % i)
        net = socket_c.receive_data("global_model_%d" % i)
        net.to(client.dev)
        print(1)
        loss_train = client.train(net, client.train_loader, client.criterion, i, n_epochs=1, save_epochs=1,
                                  device=client.dev,
                                  verbose=True)
        print(2)
        '''
        发本地模型给server
        '''
        socket_c.send_data(socket_c.conn, 'send_model', data='local_model_{}_{}'.format(i, client.name), index=i,
                           length=client.length,
                           loss=loss_train)
        i += 1
        while True:
            if socket_c.conn.recv(1024).decode(encoding='utf8') == "End of training, End of communication!":
                print("End of training, End of communication!")
                flag = 1
                break
            else:
                print("Get Model")
                break
        if flag:
            socket_c.conn.close()
            break
