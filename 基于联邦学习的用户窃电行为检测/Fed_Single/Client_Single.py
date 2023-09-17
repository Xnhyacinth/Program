#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/5/5 20:02
import copy
import json
import os
from radam import RAdam
import torch
import numpy as np
from evaluate import evaluate_fn


def test_mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


class Client(object):
    def __init__(self, name, train_loader, model_path, log_path, length, dev=torch.device("cpu")):
        self.name = name
        self.train_loader = train_loader
        self.dev = dev
        self.length = length
        self.train_loss = 0
        self.local_parameters = None
        self.model_path = model_path + "/" + name
        self.log_path = log_path

        # 模型保存路径
        test_mkdir(self.log_path)
        test_mkdir(self.model_path)

    def train_one_epoch(self, model, dataloader, optim, criterion, device=torch.device("cpu")):
        loss_sum = 0
        model.train()
        for x, y in dataloader:
            output = model(x.to(device))
            loss = criterion(output, y.to(device))
            optim.zero_grad()
            loss.backward()

            for name, parms in model.named_parameters():
                # noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                # noise_tensor = torch.Tensor(noise)
                # parms.grad.data += noise_tensor.to(device)
                if name == 'net.0.conv.conv.weight':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)
                elif name == 'net.0.conv.conv.bias':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)
                elif name == 'net.0.conv.conv1.weight':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)
                elif name == 'net.0.conv.conv1.bias':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)
                elif name == 'net.0.context.weight':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)
                elif name == 'net.0.context.bias':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)
                elif name == 'net.4.conv.conv.weight':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)
                elif name == 'net.0.conv.conv.bias':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)
                elif name == 'net.0.conv.conv1.weight':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)
                elif name == 'net.0.conv.conv1.bias':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)
                elif name == 'net.0.context.weight':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)
                elif name == 'net.0.context.bias':
                    noise = np.random.laplace(0, 1 / 50, parms.grad.shape)
                    noise_tensor = torch.Tensor(noise)
                    parms.grad.data += noise_tensor.to(device)

            optim.step()
            loss_sum += loss.item()
        return loss_sum / len(dataloader)

    def train(self, model, criterion, optim, index, n_epochs=2, save_epochs=2, verbose=False):
        for epoch in range(n_epochs):
            train_loss = self.train_one_epoch(model, self.train_loader, optim, criterion,
                                              device=self.dev)
            self.train_loss = train_loss
            if epoch % save_epochs == 0:
                save_path = os.path.join(self.model_path, 'local_model_{}'.format(index))
                torch.save(model.state_dict(), save_path)

            if verbose:
                jd = {}
                jd['communicate_index'] = index
                jd['epoch'] = epoch + 1
                jd['train_loss'] = "{:.3}".format(train_loss)

                jd = json.dumps(jd)

                with open(os.path.join(self.log_path, 'log_{}.json'.format(self.name)), 'a') as f:
                    f.write(jd + '\n')
                    f.close()

        # return model.state_dict()
        return copy.deepcopy(model.state_dict())

    def local_val(self):
        pass


class ClientsGroup(object):
    '''
        param: dataSetName 数据集的名称
        param: isIID 是否是IID
        param: numOfClients 客户端的数量
        param: dev 设备(GPU)
        param: clients_set 客户端

    '''

    def __init__(self, numOfClients, train_loader, length, model_path, log_path, dev=torch.device("cpu")):
        self.num_of_clients = numOfClients
        self.dev = dev
        self.clients_set = {}
        self.train_loader = train_loader
        self.model_path = model_path
        self.log_path = log_path
        self.dataSet(length)

    def dataSet(self, length):
        for i in range(self.num_of_clients):
            # 创建一个客户端
            name = 'client_{}'.format(i + 1)
            someone = Client(name, self.train_loader[i], self.model_path, self.log_path, length[i], dev=self.dev)
            # 为每一个clients 设置一个名字
            # clienti
            self.clients_set[name] = someone
