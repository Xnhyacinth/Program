import React from 'react'
import axios from "axios";
import {Button, Card, Table} from "antd";
import CustomBreadcrumb from "../../components/CustomBreadcrumb";


class detail extends React.Component {
    state = {
        filteredInfo: null,
        sortedInfo: null,
        loading: false,
        data: [],
        pagination: {
            pageSize: 8
        },

    }

    version_id = this.props.match.params.version_id
    tableColumns = [
        {
            title: '通信次数',
            dataIndex: 'communication',
            width: '9%',
            editable: true,
            align: 'center'
        },
        {
            title: '模型所属',
            dataIndex: 'model_tag',
            width: '9%',
            editable: true,
            align: 'center'
        },
        {
            title: '训练集损失',
            dataIndex: 'train_loss',
            width: '9%',
            editable: true,
            align: 'center'
        },
        {
            title: '验证集损失',
            dataIndex: 'valid_loss',
            width: '9%',
            editable: true,
            align: 'center'
        },
        {
            title: '准确率',
            dataIndex: 'accuracy',
            width: '8%',
            align: 'center'
        },
        {
            title: '精确率',
            dataIndex: 'precision',
            width: '8%',
            align: 'center'
        },
        {
            title: '召回率',
            dataIndex: 'recall',
            width: '8%',
            align: 'center'
        },
        {
            title: 'F1得分',
            dataIndex: 'F1',
            width: '8%',
            align: 'center'
        },
        {
            title: 'AUC',
            dataIndex: 'AUC',
            width: '6%',
            align: 'center'
        },
        {
            title: 'MAP@100',
            dataIndex: 'MAP100',
            width: '10%',
            align: 'center'
        },
        {
            title: 'MAP@200',
            dataIndex: 'MAP200',
            width: '10%',
            align: 'center'
        },
        {
            title: '模型文件',
            dataIndex: 'model',
            align: 'center',
            render: (text, record) => {
                return <div style={{textAlign: 'center'}}>
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
        /*{
            title: '操作',
            dataIndex: 'model_tag',
            align: 'center',
            render: (text, record) => {
                return <div>
                    <Button type='primary' onClick={()=>{console.log(text)}}>警告</Button>
                </div>
            }
        }*/

    ]


    loadData = () => {
        // 请求单页数据并存储到state
        var res
        var id = this.version_id
        var data = []

        function sortId(a, b) {
            return a.communication - b.communication;
        }

        axios.get('http://localhost:7777/task?taskID=' + id)
            // axios.get('http://localhost:5000/111')
            .then((response) => {
                console.log("数据加载完成")
                res = response.data
                res.ModelInfo.forEach(function (e) {
                    let tp = e.ConfusionMatrix[0]
                    let tn = e.ConfusionMatrix[1]
                    let fp = e.ConfusionMatrix[2]
                    let fn = e.ConfusionMatrix[3]
                    let precision = tp / (tp + fp) * 100
                    let recall = tp / (tp + fn) * 100
                    let F1Score = 2 * precision * recall / (precision + recall)
                    data.push({
                        communication: e.RoundNum,
                        model_tag: '全局模型',
                        F1: F1Score.toFixed(3),
                        precision: precision.toFixed(1).toString() + "%",
                        accuracy: ((tn + tp) / (tn + tp + fn + fp) * 100).toFixed(1).toString() + "%",
                        train_loss: "/",
                        valid_loss: e.Loss,
                        recall: recall.toFixed(1).toString() + "%",
                        AUC: e.AUC,
                        MAP100: (e.MAP100 * 100).toString() + "%",
                        MAP200: (e.MAP200 * 100).toString() + "%",
                    })
                })
                this.setState({partner: res.Participants},
                    () => {
                        console.log(this.state.partner)
                        this.state.partner.forEach(async function (value) {
                            await axios.get('http://localhost:7777/courts?courtsID=' + value.CourtsID)
                                // await axios.get('http://localhost:5000/' + value.CourtsID)
                                .then((response) => {
                                    res = response.data
                                    res.TrainingHistory.forEach(function (element) {
                                        if (element.TaskID === id) {
                                            element.LocalModel.forEach(function (e) {
                                                let tp = e.ConfusionMatrix[0]
                                                let tn = e.ConfusionMatrix[1]
                                                let fp = e.ConfusionMatrix[2]
                                                let fn = e.ConfusionMatrix[3]
                                                let precision = tp / (tp + fp) * 100
                                                let recall = tp / (tp + fn) * 100
                                                let F1Score = 2 * precision * recall / (precision + recall)
                                                data.push({
                                                    communication: e.RoundNum,
                                                    model_tag: value.CourtsID,
                                                    F1: F1Score.toFixed(3),
                                                    precision: precision.toFixed(1).toString() + "%",
                                                    accuracy: ((tn + tp) / (tn + tp + fn + fp) * 100).toFixed(1).toString() + "%",
                                                    train_loss: e.TrainLoss,
                                                    valid_loss: e.ValidLoss,
                                                    recall: recall.toFixed(1).toString() + "%",
                                                    AUC: e.AUC.toFixed(3),
                                                    MAP100: (e.MAP100 * 100).toFixed(1).toString() + "%",
                                                    MAP200: (e.MAP200 * 100).toFixed(1).toString() + "%",
                                                })
                                            })
                                        }
                                    })
                                    data.sort(sortId)
                                    console.log(data)
                                })
                        })
                    }
                )
            })
        return data
    }

    componentDidMount() {
        var data = this.loadData()
        setTimeout(() => {
            console.log(data)
            this.setState({
                data: data
            })
        }, 1000);
    }

    render() {
        return (
            <div>
                <CustomBreadcrumb arr={['联邦学习历史记录', `版本${(this.version_id)}`]}/>

                <Card bordered={false} title='详细信息' style={{marginBottom: 10, minHeight: 440}}>
                    <Table style={styles.tableStyle} bordered dataSource={this.state.data}
                           columns={this.tableColumns} pagination={{pageSize: 8}}/>
                    <p>
                        {this.state.court_num}个台区参与通信{this.state.data.length / 4}次

                    </p>
                    <p>
                        共有{this.state.data.length}条记录
                    </p>
                </Card>
            </div>
        )
    }
}

const styles = {
    tableStyle: {
        width: '90%',
        marginLeft: '5%'
    }
}


export default detail