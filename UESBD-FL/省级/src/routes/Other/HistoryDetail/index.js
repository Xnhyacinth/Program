import React from 'react'
import axios from "axios";
import { Button, Card, Table } from "antd";
import CustomBreadcrumb from "../../../components/CustomBreadcrumb";

const data = [];

for (let i = 0; i < 8; i++) {
    data.push({
        key: '1',
        communication: 1,
        model_tag: "全局模型",
        date: '2022-5-12',
        F1: 0.048,
        precision: "91.6%",
        accuracy: "64.3%",
        train_loss: "/",
        valid_loss: 0.284,
        recall: "2.5%",
        AUC: 0.687,
        MAP100: "62.5%",
        MAP200: "63.7%",
    })
    data.push({
        key: '2',
        communication: 1,
        model_tag: "C001",
        date: '2022-5-12',
        F1: 0.011,
        precision: "66.7%",
        accuracy: "91.5%",
        train_loss: 0.448,
        valid_loss: 0.386,
        recall: "0.5%",
        AUC: 0.700,
        MAP100: "59.6%",
        MAP200: "64.2%",
    })
    data.push({
        key: '3',
        communication: 1,
        model_tag: "C002",
        date: '2022-5-12',
        F1: 0.016,
        precision: "75%",
        accuracy: "91.5%",
        train_loss: 0.346,
        valid_loss: 0.334,
        recall: "0.8%",
        AUC: 0.697,
        MAP100: "52.4%",
        MAP200: "57.3%",
    })
    data.push({
        key: '4',
        communication: 2,
        model_tag: "C003",
        date: '2022-5-12',
        F1: 0.027,
        precision: "83.3%",
        accuracy: "91.6%",
        train_loss: 0.34,
        valid_loss: 0.28,
        recall: "1.3%",
        AUC: 0.716,
        MAP100: "69.6%",
        MAP200: "69.2%",
    })
    data.push({
        key: '5',
        communication: 2,
        model_tag: "全局模型",
        date: '2022-5-12',
        F1: 0.064,
        precision: "80.0%",
        accuracy: "91.7%",
        train_loss: "/",
        valid_loss: 0.269,
        recall: "3.3%",
        AUC: 0.711,
        MAP100: "65.8%",
        MAP200: "66.1%",
    })
    data.push({
        key: '6',
        communication: 2,
        model_tag: "C001",
        date: '2022-5-12',
        F1: 0.00,
        precision: "0.0%",
        accuracy: "91.5%",
        train_loss: 0.292,
        valid_loss: 0.294,
        recall: "0.5%",
        AUC: 0.719,
        MAP100: "36.7%",
        MAP200: "46.8%",
    })
    data.push({
        key: '7',
        communication: 2,
        model_tag: "C002",
        date: '2022-5-12',
        F1: 0.011,
        precision: "50%",
        accuracy: "91.5%",
        train_loss: 0.296,
        valid_loss: 0.278,
        recall: "0.5%",
        AUC: 0.728,
        MAP100: "49.8%",
        MAP200: "55.6%",
    })
    data.push({
        key: '8',
        communication: 2,
        model_tag: "C003",
        date: '2022-5-12',
        F1: 0.038,
        precision: "100%",
        accuracy: "91.6%",
        train_loss: 0.283,
        valid_loss: 0.273,
        recall: "1.9%",
        AUC: 0.72,
        MAP100: "74.7%",
        MAP200: "69.9",
    })
    data.push({
        key: '9',
        communication: 3,
        model_tag: "全局模型",
        date: '2022-5-12',
        F1: 0.022,
        precision: "57.1%",
        accuracy: "91.5%",
        train_loss: "/",
        valid_loss: 0.256,
        recall: "1.1%",
        AUC: 0.760,
        MAP100: "44.4%",
        MAP200: "46.1%",
    })
    data.push({
        key: '10',
        communication: 3,
        model_tag: "C001",
        date: '2022-5-12',
        F1: 0.016,
        precision: "71.5%",
        accuracy: "91.5%",
        train_loss: 0.277,
        valid_loss: 0.289,
        recall: "0.8%",
        AUC: 0.745,
        MAP100: "60.2%",
        MAP200: "61.9%",
    })
}


class detail extends React.Component {
    state = {
        filteredInfo: null,
        sortedInfo: null,
        loading: false,
        pagination: {
            pageSize: 8
        },
        communication: 0,
        court_num: 0,
        data,
        editingKey: '',
    }
    version_id = this.props.match.params.version_id
    columns = [
        {
            title: '通信次数',
            dataIndex: 'communication',
            width: '9%',
            editable: true,
        },
        {
            title: '模型所属',
            dataIndex: 'model_tag',
            width: '9%',
            editable: true,
        },
        {
            title: '训练集损失',
            dataIndex: 'train_loss',
            width: '9%',
            editable: true,
        },
        {
            title: '验证集损失',
            dataIndex: 'valid_loss',
            width: '9%',
            editable: true,
        },
        {
            title: '准确率',
            dataIndex: 'accuracy',
            width: '8%',
        },
        {
            title: '精确率',
            dataIndex: 'precision',
            width: '8%',
        },
        {
            title: '召回率',
            dataIndex: 'recall',
            width: '8%',
        },
        {
            title: 'F1得分',
            dataIndex: 'F1',
            width: '8%',
        },
        {
            title: 'AUC',
            dataIndex: 'AUC',
            width: '6%',
        },
        {
            title: 'MAP@100',
            dataIndex: 'MAP100',
            width: '10%',
        },
        {
            title: 'MAP@200',
            dataIndex: 'MAP200',
            width: '10%',
        },
        {
            title: '模型文件',
            dataIndex: 'model',
            render: (text, record) => {
                return <div style={{ textAlign: 'center' }}>
                    <Button type="primary" shape="round" onClick={() => {
                        axios({
                            url: '', //调用的接口，该接口返回文件流
                            method: 'get',
                            params: {
                                //接口的参数
                                model_tag: record.model_tag,
                                version: text.toString()
                            },
                            responseType: 'blob',
                        }).then((response) => {
                            const url = window.URL.createObjectURL(new Blob([response.data]));
                            const link = document.createElement('a');
                            link.href = url;
                            link.setAttribute('download', `${record.model_tag}_version${text}`); //下载后的文件名{tag}_version{id}
                            document.body.appendChild(link);
                            link.click();
                        });
                    }}>
                        下载
                    </Button>

                </div>

            }
        },

    ]

    componentDidMount() {
        // 请求单页数据并存储到state
        axios.get("http://jsonplaceholder.typicode.com/posts/" + this.version_id).then(res => {
            this.setState({
                post: res.data
            })
        })
        this.setState({
            communication: 3,
            court_num: 3,
        })
    }

    render() {

        // 从state中取出数据并加工
        // const {post} = this.state;
        // const postShow = post ? (
        //     <div className='collection-item' key={post.id}>
        //         <h3 className='center'>{post.title}</h3>
        //         <p>{post.body}</p>
        //     </div>
        // ) : (
        //     <div className='center'>还在加载中......</div>
        // )
        return (
            <div>
                <CustomBreadcrumb arr={['联邦学习历史记录', `版本${(this.version_id)}`]} />

                <Card bordered={false} title='详细信息' style={{ marginBottom: 10, minHeight: 440 }} id='editTable'>
                    <Table style={styles.tableStyle} bordered dataSource={this.state.data}
                        columns={this.columns} />
                    <p>
                        {this.state.court_num}个台区参与通信20次

                    </p>
                    <p>
                        共有{data.length}条记录
                    </p>
                </Card>
            </div>
        )
    }
}

const styles = {
    tableStyle: {
        width: '90%'
    },
    affixBox: {
        position: 'absolute',
        top: 100,
        right: 50,
        with: 170
    }
}


export default detail