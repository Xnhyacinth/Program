#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/5/5 16:32
import argparse
import copy
import math
from torch import nn
from torch.optim import SGD
from torch.utils.data import DataLoader
from evaluate import evaluate_fn
from metrics import metrics_report
from Client_Single import *
from Hybrid_Attn import HybridAttentionModel
from radam import RAdam
from dataset import FraudDataset
from data import *
from tqdm import tqdm

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="FedAvg")
parser.add_argument('-g', '--gpu', type=str, default='0', help='gpu id to use(e.g. 0,1,2,3)')
# 客户端的数量
parser.add_argument('-nc', '--num_of_clients', type=int, default=3, help='number of the clients')
# 随机挑选的客户端的数量
parser.add_argument('-cf', '--cfraction', type=float, default=1,
                    help='C fraction, 0 means 1 client, 1 means total clients')
# 训练次数(客户端更新次数)
parser.add_argument('-E', '--epoch', type=int, default=1, help='local train epoch')
# batchsize大小
parser.add_argument('-B', '--batchsize', type=int, default=100, help='local train batch size')
# 学习率
parser.add_argument('-lr', "--learning_rate", type=float, default=0.001, help="learning rate, \
                    use value from origin paper as default")
# n um_comm 表示通信次数，此处设置为20
parser.add_argument('-ncomm', '--num_comm', type=int, default=20, help='number of communications')
# 保存频率
parser.add_argument('-sf', '--save_freq', type=int, default=1, help='global model save frequency(of communication)')
# 数据路径
parser.add_argument('-d', '--data_path', type=str, default='data/data_train_', help='data path')
# 模型路径
parser.add_argument('-m', '--model_path', type=str, default='./model', help='model path')
# 日志路径
parser.add_argument('-l', '--log_path', type=str, default='./log', help='log path')
# 结果路径
parser.add_argument('-r', '--result_path', type=str, default='./result', help='result path')
# 聚合算法
parser.add_argument('-a', '--aggregation', type=str, default='FedAvg', help='aggregation algorithm')
# 优化器
parser.add_argument('-opt', '--optimizer', type=str, default='RAdam', help='optimizer')


def test_mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def FedAvg(models, lengths):
    """
    根据样本数量来聚合
    将模型进行聚合
    """
    l = sum(lengths)
    m = {}
    for k, v in models[0].items():
        m[k] = copy.deepcopy(v)
        m[k] = m[k] * (lengths[0] / l)
    for j in range(1, len(models)):
        for k, v in models[j].items():
            m[k] += v * (lengths[j] / l)
    return m


def FedAvg_LA(models, losses):
    """
    根据客户端模型的损失占比来聚合
    将模型进行聚合
    """
    m = {}
    for k, v in models[0].items():
        m[k] = copy.deepcopy(v)
        m[k] = m[k] * (losses[0] / sum(losses))
    for j in range(1, len(models)):
        for k, v in models[j].items():
            m[k] += v * (losses[j] / sum(losses))
    return m


def FedAvg_LS(models, lengths, losses):
    """
    根据样本数量和客户端模型的损失占比来聚合
    """
    m = {}
    sum_loss = sum(map(lambda x, y: x * y, losses, lengths))
    for k, v in models[0].items():
        m[k] = copy.deepcopy(v)
        m[k] = m[k] * (losses[0] * lengths[0] / sum_loss)
    for j in range(1, len(models)):
        for k, v in models[j].items():
            m[k] += v * (losses[j] * lengths[j] / sum_loss)
    return m


def model_eval(index, m, dataloader, name, loss_func, dev):
    """
    模型评估
    """
    m.to(device)
    valid_loss, tn, fp, fn, tp, precision, recall, f1Score = evaluate_fn(m, dataloader, loss_func, dev, verbose=True)
    jd = {}
    jd['communicate_index'] = index + 1
    jd['valid_loss'] = "{:.3}".format(valid_loss)
    jd['tn'] = "{}".format(tn)
    jd['fp'] = "{}".format(fp)
    jd['fn'] = "{}".format(fn)
    jd['tp'] = "{}".format(tp)
    jd['accuracy'] = "{:.3}".format((tn + tp) / (tn + tp + fn + fp))
    jd['precision'] = "{:.3}".format(precision)
    jd['recall'] = "{:.3}".format(recall)
    jd['f1Score'] = "{:.3}".format(f1Score)
    # 写入结果
    metrics_report(model, dataloader, jd, name=name, device=dev)


def cal_contribution(loss, score, index, c):
    """
    计算贡献度
    """
    loss_sum = sum(loss)
    s_index = {}
    if index:
        for j in range(len(loss)):
            q = 1 - loss[j] / loss_sum
            s = (score[index - 1][c[j]] * index + 1 / (1 + math.exp(-math.log(q)))) / (index + 1)
            s_index[c[j]] = s
    else:
        for j in range(len(loss)):
            q = 1 - loss[j] / loss_sum
            s = 1 / (1 + math.exp(-math.log(q)))
            s_index[c[j]] = s
    score.append(s_index)
    return s_index


if __name__ == "__main__":
    # 获取参数
    args = parser.parse_args()
    args = args.__dict__
    # 创建文件夹
    test_mkdir(args['model_path'])
    test_mkdir(args['log_path'])
    test_mkdir(args['result_path'])

    # 创建模型
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    # device = torch.device("cpu")
    model = HybridAttentionModel().to(device)

    optimizer = None
    if args['optimizer'] == 'RAdam':
        # 创建模型的优化器
        optimizer = RAdam(model.parameters(), lr=args['learning_rate'])
    elif args['optimizer'] == 'Adam':
        optimizer = RAdam(model.parameters(), lr=args['learning_rate'])
    elif args['optimizer'] == 'SGD':
        optimizer = SGD(model.parameters(), lr=args['learning_rate'])

    # 损失函数
    criterion = nn.CrossEntropyLoss()

    # 创建模型的学习率衰减
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

    # 创建模型的训练集
    data_length = [8000, 14000, 16135]
    train_datasets = [GetDataSet(path) for path in list(set((args['data_path'] + str(d) + ".csv") \
                                                            for d in data_length \
                                                            for _ in range(args['num_of_clients'])))]

    train_loaders = [DataLoader(dataset=train_set, batch_size=args['batchsize'], shuffle=True) \
                     for train_set in map(lambda x: FraudDataset(x[0], x[1]), train_datasets)]

    # 创建模型的测试集
    X_eval, y_eval = GetDataSet('data/eval.csv')
    dataset_eval = FraudDataset(X_eval, y_eval)

    valid_loader = DataLoader(dataset=dataset_eval, batch_size=args['batchsize'], shuffle=False)

    # 创建Clients
    myClients = ClientsGroup(args['num_of_clients'], train_loaders, data_length, args['model_path'], args['log_path'],
                             dev=device)

    # 每次随机选取3个Clients
    num_in_comm = int(max(args['num_of_clients'] * args['cfraction'], 1))

    # 得到全局的参数
    global_parameters = {}
    for key, var in model.state_dict().items():
        global_parameters[key] = var.clone()

    scores = []  # 贡献度
    # 通信次数
    for i in range(args['num_comm']):
        # 将5个客户端进行随机排序
        order = np.random.permutation(args['num_of_clients'])

        # 生成客户端
        clients_in_comm = ['client_{}'.format(i + 1) for i in order[0:num_in_comm]]

        # 每轮聚合模型参数和
        sum_parameters = None
        # 每个Client基于当前模型参数和自己的数据训练并更新模型
        # 返回每个Client更新后的参数
        # 这里的clients_
        params = []  # 参数
        losses = []  # 损失
        length = []  # 样本数
        clients = []  # 客户端
        for client in tqdm(clients_in_comm):
            # 获取当前Client训练得到的参数
            # 这一行代码表示Client端的训练函数，我们详细展开：
            # local_parameters 得到客户端的局部变量
            model.load_state_dict(global_parameters)
            model.to(device)
            local_parameters = myClients.clients_set[client].train(model, criterion, optimizer, i + 1,
                                                                   n_epochs=args['epoch'],
                                                                   save_epochs=args['save_freq'], verbose=True)
            params.append(local_parameters)
            length.append(myClients.clients_set[client].length)
            losses.append(myClients.clients_set[client].train_loss)
            clients.append(myClients.clients_set[client].name)

            # eval client model
            model_eval(i, model, valid_loader, myClients.clients_set[client].name, criterion, device)

            # 对所有的Client返回的参数累加（最后取平均值）
            if sum_parameters is None:
                sum_parameters = {}
                for key, var in local_parameters.items():
                    sum_parameters[key] = var.clone()
            else:
                for var in sum_parameters:
                    sum_parameters[var] = sum_parameters[var] + local_parameters[var]

        '''
        计算贡献度
        '''
        contributions = cal_contribution(losses, scores, i, clients)
        if i == args['num_comm'] - 1:
            for c in clients:
                jd = {}
                jd = {'client': c, 'contribution': "{:.4}".format(contributions[c] * 100)}
                jd = json.dumps(jd, ensure_ascii=False)
                with open(os.path.join("./", 'log/log_{}.json'.format(c)), 'a') as f:
                    f.write(jd + '\n')
                    f.close()
        if args['aggregation'] == 'Average':
            '''
            对所有的Client返回的参数累加（最后取平均值）
            '''
            # 取平均值，得到本次通信中Server得到的更新后的模型参数
            for var in global_parameters:
                global_parameters[var] = (sum_parameters[var] / num_in_comm)
            # save server model
            model.load_state_dict(global_parameters, strict=True)
            # torch.save(model, args['model_path'] + '/avg' + 'global_model_{}'.format(i + 1))
            # model eval
            model_eval(i, model, valid_loader, 'avg', criterion, device)
        elif args['aggregation'] == 'FedAvg':
            '''
            FedAvg
            '''
            global_parameters = FedAvg(params, length)
            # save server model
            model.load_state_dict(global_parameters, strict=True)
            # torch.save(model, args['model_path'] + '/normal' + 'global_model_{}'.format(i + 1))
            # model eval
            model_eval(i, model, valid_loader, 'normal', criterion, device)
        elif args['aggregation'] == 'LA':
            '''
            LA
            '''
            global_parameters = FedAvg_LA(params, losses)
            # save server model
            model.load_state_dict(global_parameters, strict=True)
            # torch.save(model, args['model_path'] + '/LA' + 'global_model_{}'.format(i + 1))
            # model eval
            model_eval(i, model, valid_loader, 'LA', criterion, device)
        else:
            '''
            LS
            '''
            global_parameters = FedAvg_LS(params, length, losses)
            # save server model
            model.load_state_dict(global_parameters, strict=True)
            # torch.save(model, args['model_path'] + '/LS' + 'global_model_{}'.format(i + 1))
            # model eval
            model_eval(i, model, valid_loader, 'LS', criterion, device)
