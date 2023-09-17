#!/usr/bin/env python3
# _*_coding:utf-8_*_
# @Author : Xnhyacinth
# @Time : 2022/4/22 15:33

from torch import nn
from Client import *
from Server_Socket import *
import sys
from Hybrid_Attn import HybridAttentionModel
from radam import RAdam
from data import *

sys.setrecursionlimit(1000000)

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="FedAvg")
parser.add_argument('-g', '--gpu', type=str, default='0', help='gpu id to use(e.g. 0,1,2,3)')
# 客户端的数量
parser.add_argument('-nc', '--num_of_clients', type=int, default=3, help='numer of the clients')
# 随机挑选的客户端的比例
parser.add_argument('-cf', '--cfraction', type=float, default=1,
                    help='C fraction, 0 means 1 client, 1 means total clients')
# 训练次数(客户端更新次数)
parser.add_argument('-E', '--epoch', type=int, default=2, help='local train epoch')
# batchsize大小
parser.add_argument('-B', '--batchsize', type=int, default=64, help='local train batch size')
# 学习率
parser.add_argument('-lr', "--learning_rate", type=float, default=0.001, help="learning rate, \
                    use value from origin paper as default")
# 模型验证频率（通信频率）
parser.add_argument('-vf', "--val_freq", type=int, default=5, help="model validation frequency(of communications)")
parser.add_argument('-sf', '--save_freq', type=int, default=20, help='global model save frequency(of communication)')
# n um_comm 表示通信次数，此处设置为20
parser.add_argument('-ncomm', '--num_comm', type=int, default=20, help='number of communications')
parser.add_argument('-sp', '--save_path', type=str, default='./log', help='the saving path of checkpoints')
# 端口
parser.add_argument('-p', '--port', type=int, default=8182, help='the port of communication')


def test_mkdir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


if __name__ == "__main__":
    args = parser.parse_args()
    args = args.__dict__

    os.environ['CUDA_VISIBLE_DEVICES'] = args['gpu']
    dev = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    # 启动服务器
    server = Server(int(args['num_of_clients'] * args['cfraction']), args['num_comm'], dev)

    # -----------------------文件保存-----------------------#
    test_mkdir(args['save_path'])
    test_mkdir('./result')

    # 初始化模型
    # 对卷积核进行he_normal
    net = HybridAttentionModel().to(dev)
    # torch.nn.init.kaiming_normal_(net.deep_component_conv.weight)

    # 定义损失函数
    loss_func = nn.CrossEntropyLoss()

    # 定义学习率
    lr = 0.001

    # 定义优化函数
    opti = RAdam(net.parameters(), lr)

    # 创建Clients
    # myClients = ClientsGroup(args['num_of_clients'], dev, args['port'])
    # testDataLoader = myClients.test_data_loader

    # 每次随机选取3个Clients
    num_in_comm = int(max(args['num_of_clients'] * args['cfraction'], 1))

    # 得到全局的参数
    global_parameters = {}
    # torch.save(net.state_dict(), "global_model_0")
    torch.save(net, "global_model_0")

    # 得到每一层中全连接层中的名称
    # 以及权重weights(tenor)
    # 得到网络每一层上
    # for key, var in net.state_dict().items():
    #     # print("key:"+str(key)+",var:"+str(var))
    #     # print("张量的维度:" + str(var.shape))
    #     # print("张量的Size" + str(var.size()))
    #     global_parameters[key] = var.clone()

    # 新开一个线程，用于接收新连接
    thread = Thread(target=server.accept_client)
    thread.setDaemon(True)
    thread.start()
    # 主线程逻辑
    while True:
        time.sleep(0.1)
        if server.send:
            for client_type, client in server.g_conn_pool.items():
                client.sendall("End of Aggregating".encode(encoding='utf8'))
            # 初始化
            server.sum_parameters = {}
            server.global_parameters = {}
            server.sum_client = 0
            server.send = 0
            server.length = []
            server.params = []
            server.losses = []
            server.clients = []
        if server.flag:
            clients = []
            print("End of training, End of communication!")
            for client_type, client in server.g_conn_pool.items():
                client.sendall("End of training, End of communication!".encode(encoding='utf8'))
                clients.append(client_type)
            break

    # 获取最优模型结果
    net = torch.load('global_model_{}'.format(server.best_com))
    net.to(dev)
    # 得到最优模型的结果
    valid_loss, tn, fp, fn, tp, precision, recall, f1Score = evaluate_fn(net, server.valid_loader,
                                                                         loss_func,
                                                                         dev, verbose=True)
    jd = {}
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
    metrics_report(net, server.valid_loader, jd, name="best_model", device=dev)
