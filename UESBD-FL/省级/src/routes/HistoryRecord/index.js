import React from 'react'
import {Button, Table, BackTop} from 'antd'
import axios from 'axios'
import CustomBreadcrumb from '../../components/CustomBreadcrumb'

class HistoryRecord extends React.Component {
    state = {
        historyData: [],
    }

    loadData = () => {
        var data = [];
        var res = [{
            "docType": "globalmodelObj",
            "TaskID": "Task1",
            "TaskDescription": {
                "Round": 20,
                "AggAlgorithm": "FedAvg",
                "OptimAlgorithm": "RAdam",
                "Lr": 0.001,
                "IfDP": "否",
                "Epsilon": 0,
                "SimpleDescription": "基于多头注意力机制的窃电行为检测模型"
            },
            "FinalLoss": 0.018,
            "FinalAccuracy": 0.9576,
            "FinalRecall": 0.905,
            "FinalF1": 0.932,
            "FinalConfusionMatrix": [3825, 51, 171, 191],
            "Participants": [{"CourtsID": "Courts1", "Contribution": 50.65}, {
                "CourtsID": "Courts2",
                "Contribution": 50
            }, {"CourtsID": "Courts3", "Contribution": 48.72}],
            "ModelInfo": [{
                "RoundNum": 1,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 2,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 3,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 4,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 5,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 6,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 7,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 8,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 9,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 10,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 11,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 12,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 13,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 14,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 15,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 16,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 17,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 18,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 19,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }, {
                "RoundNum": 20,
                "Loss": 0.284,
                "AUC": 0.905,
                "MAP100": 0.765,
                "MAP200": 0.658,
                "ConfusionMatrix": [3825, 51, 171, 191],
                "IPFSHash": "ABC76F4ER78S946ABC76F4ER78S946ABC76F4ER78S9465"
            }]
        }]
        let i = 1
        res.forEach(function (e) {
            data.push({
                key: i,
                taskID: e.TaskID,
                trainingDate: "2022-4-12",
                finalAccuracy: e.FinalAccuracy,
                model_tag: "全局模型",
                taskDescription: e.TaskDescription.SimpleDescription,
                modelHash: e.ModelInfo[e.ModelInfo.length - 1].IPFSHash,
                modelInfo: e.ModelInfo,
                partner: e.Participants
            })
            i += 1
        })
        axios.get('http://localhost:7777//alltask')
            .then((response) => {
                console.log("数据加载完成")
                res = response.data
                let i = 1
                res.forEach(function (e) {
                    data.push({
                        key: i,
                        taskID: e.TaskID,
                        trainingDate: e.TaskDescription.Time,
                        finalAccuracy: e.FinalAccuracy,
                        model_tag: "全局模型",
                        taskDescription: e.TaskDescription.SimpleDescription,
                        modelHash: e.ModelInfo[e.ModelInfo.length - 1].IPFSHash,
                        modelInfo: e.ModelInfo,
                        partner: e.Participants
                    })
                    i += 1
                })
                this.setState({
                    historyData: data
                })
            })
    }

    componentDidMount() {
        this.loadData()
    }

    columns = [
        {
            title: '版本编号',
            dataIndex: 'taskID',
            width: '8%',
            editable: true,
            align: 'center'
        },
        {
            title: '训练日期',
            dataIndex: 'trainingDate',
            width: '13%',
            editable: true,
            align: 'center'
        },
        {
            title: '最终模型准确率',
            dataIndex: 'finalAccuracy',
            width: '11%',
            editable: true,
            align: 'center'
        },
        {
            title: '描述',
            dataIndex: 'taskDescription',
            width: '45%',
            editable: true,
            align: 'center'
        },
        {
            title: '模型文件',
            dataIndex: 'taskID',
            align: 'center',
            render: (text, record) => {
                return <div style={{textAlign: 'center'}}>
                    <Button type="primary" shape="round" onClick={() => {
                        axios({
                            url: 'http://127.0.0.1:5000/download', //调用的接口，该接口返回文件流
                            method: 'get',
                            params: {
                                //接口的参数
                                model_tag: record.model_tag,
                                version: text.toString(),
                                hash: record.modelHash,
                                date: record.trainingDate
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
        {
            title: '查看详情',
            dataIndex: 'taskID',
            align: 'center',
            render: (text, record) => {
                console.log(record.modelInfo)
                return <div style={{textAlign: 'center'}}>
                    <Button type="primary" shape="round" onClick={() => {
                        this.props.history.push({
                            pathname: '/home/historyrecord/' + text.toString(),
                            state: {
                                version_id: text,
                                modelInfo: record.modelInfo,
                                partner: record.partner,
                                date: record.trainingDate
                            }

                        })
                    }}>
                        详情
                    </Button>

                </div>

            }
        },
    ]

    render() {
        return (
            <div>
                <CustomBreadcrumb arr={['联邦学习历史记录']}/>

                <Table style={styles.tableStyle} bordered dataSource={this.state.historyData}
                       columns={this.columns}/>
                <p>
                    共有{this.state.historyData.length}条记录
                </p>
                <BackTop visibilityHeight={200} style={{right: 50}}/>

            </div>
        )
    }
}

const
    styles = {
        tableStyle: {
            width: '90%',
            'margin-left': '5%'
        },
        affixBox: {
            position: 'absolute',
            top: 100,
            right: 50,
            with: 170
        }
    }


export default HistoryRecord