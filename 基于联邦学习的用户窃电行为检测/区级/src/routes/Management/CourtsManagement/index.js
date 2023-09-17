import React from 'react'
import {Card, Switch, Badge, Button, Table, BackTop, Modal, Input, Col} from 'antd'
import 'antd/dist/antd.css';
import axios from 'axios'
import CustomBreadcrumb from '../../../components/CustomBreadcrumb/index'
import '../CourtsManagement/style.css'

var epsilon = ""
var flagEpsilon = false
var userNum = ""
var flagUserNum = false

class CourtsManagement extends React.Component {
    state = {
        courtsInfo: [],
        modalEditVisible: false, //是否显示编辑对话框
        currentSelect: [],
    }

    currentSelect = []

    //设置是否显示编辑对话框
    setEditModalVisible(modalEditVisible) {
        this.setState({modalEditVisible});
    }

    //开启台区操作
    courtsOnline = (record) => {
        //1.调用链码服务，修改台区状态
        /*
            Todo
        */
        console.log(record.courtsUserNum)
        // axios.post('http://localhost:7777/setcourtsinfo?courtsID=' + record.courtsID, {
        //     State: record.courtsStatus,
        //     ConsumerCount: record.courtsUserNum,
        //     Reputation: record.courtsEpsilon
        // })
        //2.修改状态
        var newCourts = this.state.courtsInfo
        for (var i = 0; i < newCourts.length; i++) {
            if (newCourts[i].index === record.index) {
                newCourts[i].courtsStatus = (record.courtsStatus === "在线" ? "离线" : "在线")
                break
            }
        }
        this.setState({
            courtsInfo: newCourts,
        })
    }

    //修改台区信息操作
    ClickeditInfo = (record) => {
        //1.获取当前选值
        this.currentSelect = record
        //弹出对话框
        this.setEditModalVisible(true)

    }

    getEpsilon = (e) => {
        e.persist()
        epsilon = e.target.value
        flagEpsilon = true
    }

    getUserNum = (e) => {
        e.persist()
        userNum = e.target.value
        flagUserNum = true
    }

    //在对话框上点击了确认按钮之后的操作
    handleOK = () => {
        //1.调用链码服务修改台区地址和用户数量
        /*
            Todo
        */
        console.log(this.currentSelect)
        // axios.post('http://localhost:7777/setcourtsinfo?courtsID=' + this.currentSelect.courtsID, {
        //     State: this.currentSelect.courtsStatus,
        //     ConsumerCount: this.currentSelect.courtsUserNum,
        //     Reputation: this.currentSelect.courtsEpsilon
        // })
        //2.修改台区信息
        var newCourtsInfo = this.state.courtsInfo
        if (flagEpsilon === true) {
            for (var i = 0; i < newCourtsInfo.length; i++) {
                if (newCourtsInfo[i].index === this.currentSelect.index) {
                    newCourtsInfo[i].courtsEpsilon = epsilon
                    break
                }
            }
        }
        if (flagUserNum === true) {
            for (i = 0; i < newCourtsInfo.length; i++) {
                if (newCourtsInfo[i].index === this.currentSelect.index) {
                    newCourtsInfo[i].courtsUserNum = userNum
                    break
                }
            }
        }
        this.setState({
            courtsInfo: newCourtsInfo
        })

        this.setEditModalVisible(false)
    }

    //台区信息展示列表项
    tableColumns = [
        {
            title: '序号',
            dataIndex: 'index',
            width: '8%',
            editable: true,
            align: 'center'
        },
        {
            title: '台区编号',
            dataIndex: 'courtsID',
            width: '15%',
            editable: true,
            align: 'center'
        },
        {
            title: '地址',
            dataIndex: 'courtsAddress',
            width: '20%',
            editable: true,
            align: 'center'
        },
        {
            title: '用户数量',
            dataIndex: 'courtsUserNum',
            width: '12%',
            editable: true,
            align: 'center'
        },
        {
            title: '历史贡献度',
            dataIndex: 'courtsContribution',
            width: '12%',
            editable: true,
            align: 'center'
        },
        {
            title: '隐私预算',
            dataIndex: 'courtsEpsilon',
            width: '12%',
            editable: true,
            align: 'center'
        },
        {
            title: '状态',
            dataIndex: 'courtsStatus',
            render: (text, record) => {
                return <div>
                    {text === "在线" ? <Badge status="success" text="在线"/> : <Badge status="default" text="离线"/>}
                    <Switch style={{"margin-left": 10, "marginBottom": 5}} checkedChildren="开启" unCheckedChildren="关闭"
                            defaultChecked={text === "在线" ? true : false} onChange={() => this.courtsOnline(record)}/>
                </div>
            },
            align: 'center'
        },
        {
            title: '操作',
            render: (record) => {
                return <Button type="primary" onClick={() => this.ClickeditInfo(record)}>修改</Button>
            },
            align: 'center'
        },
    ]

    //加载数据
    loadData = () => {
        var data
        var staticData = []

        function sum(arr) {
            var s = 0;
            for (var i = arr.length - 1; i >= 0; i--) {
                s += arr[i];
            }
            return s;
        }

        let contribution = []

        function cal_contribution(e) {
            e.TrainingHistory.forEach(function (element) {
                console.log(element)
                contribution.push(element.Contribution)
            })
            console.log(contribution)
            return sum(contribution)
        }

        // data = [{
        //     "docType": "courtstrainingObj", "CourtsID": "C001", "district": "北京昌平区", "State": "在线",
        //     "Address": "北京市昌平区xx路xx号", "ConsumerCount": 5726, "Reputation": 50,
        //     "TrainingHistory": [
        //         {
        //             "TaskID": "Task1", "Contribution": 40.24,
        //             "LocalModel": [
        //                 {
        //                     "RoundNum": 1,
        //                     "TrainLoss": 0.381,
        //                     "ValidLoss": 0.302,
        //                     "AUC": 0.703,
        //                     "MAP100": 0.51,
        //                     "MAP200": 0.56,
        //                     "ConfusionMatrix": [3875, 1, 361, 0],
        //                     "IPFSHash": "ABC76F4ER78S946"
        //                 },
        //                 {
        //                     "RoundNum": 2,
        //                     "TrainLoss": 0.289,
        //                     "ValidLoss": 0.298,
        //                     "AUC": 0.7,
        //                     "MAP100": 0.638,
        //                     "MAP200": 0.657,
        //                     "ConfusionMatrix": [3875, 1, 361, 0],
        //                     "IPFSHash": "ABC76F4ER78S946"
        //                 }]
        //         },
        //         {
        //             "TaskID": "Task2", "Contribution": 40.24,
        //             "LocalModel": [
        //                 {
        //                     "RoundNum": 1,
        //                     "TrainLoss": 0.381,
        //                     "ValidLoss": 0.302,
        //                     "AUC": 0.703,
        //                     "MAP100": 0.51,
        //                     "MAP200": 0.56,
        //                     "ConfusionMatrix": [3875, 1, 361, 0],
        //                     "IPFSHash": "ABC76F4ER78S946"
        //                 },
        //                 {
        //                     "RoundNum": 2,
        //                     "TrainLoss": 0.289,
        //                     "ValidLoss": 0.298,
        //                     "AUC": 0.7,
        //                     "MAP100": 0.638,
        //                     "MAP200": 0.657,
        //                     "ConfusionMatrix": [3875, 1, 361, 0],
        //                     "IPFSHash": "ABC76F4ER78S946"
        //                 }]
        //         }]
        // }]
        // data.forEach(function (e) {
        //     staticData.push({
        //         index: 1,
        //         courtsID: e.CourtsID,
        //         courtsAddress: e.Address,
        //         courtsUserNum: e.ConsumerCount,
        //         courtsContribution: cal_contribution(e),
        //         courtsStatus: e.State,
        //         courtsEpsilon: e.Reputation
        //     });
        // })

        axios.get('http://localhost:7777/courts?courtsID=C001')
            .then(function (response) {
                console.log("数据加载完成")
                data = response.data
                let i = 1
                data.forEach(function (e) {
                    staticData.push({
                        index: i,
                        courtsID: e.courtsID,
                        courtsAddress: e.Address,
                        courtsUserNum: e.ConsumerCount,
                        courtsContribution: cal_contribution(e),
                        courtsStatus: e.State,
                        courtsEpsilon: e.Reputation
                    });
                    i += 1
                })
                this.setState({
                    courtsInfo: staticData,
                })
            })
    }

    //加载页面时执行
    componentDidMount() {
        this.loadData()
    }

    render() {
        return (
            <div>
                <CustomBreadcrumb arr={['信息管理', '台区信息管理']}/>
                <Card bordered={false} title='台区信息' style={{marginBottom: 10, minHeight: 440}}>
                    <Table style={styles.tableStyle} bordered dataSource={this.state.courtsInfo}
                           columns={this.tableColumns}/>

                    <Modal
                        title="修改台区信息"
                        centered
                        visible={this.state.modalEditVisible}
                        onOk={() => this.handleOK()}
                        onCancel={() => this.setEditModalVisible(false)}
                    >

                        <div style={{"display": "flex"}}>
                            <Col span={12}>
                                <Card>
                                    <Col span={12}>
                                        台区编号:
                                    </Col>
                                    <Col span={12}>
                                        {this.currentSelect.courtsID}
                                    </Col>
                                </Card>
                            </Col>
                            <Col span={12}>
                                <Card>
                                    <Col span={12}>
                                        历史贡献度:
                                    </Col>
                                    <Col span={12}>
                                        {this.currentSelect.courtsContribution}
                                    </Col>
                                </Card>
                            </Col>
                        </div>


                        <Card>
                            <p>用户数量:</p>
                            <Input style={{"margin-bottom": 10}} defaultValue={this.currentSelect.courtsUserNum}
                                   onChange={this.getUserNum}/>
                        </Card>

                        <Card>
                            <p>隐私预算:</p>
                            <Input style={{"margin-bottom": 10}} allowClear
                                   defaultValue={this.currentSelect.courtsEpsilon} onChange={this.getEpsilon}/>
                        </Card>
                    </Modal>
                </Card>
            </div>
        )
    }
}

const
    styles = {
        tableStyle: {
            width: '90%',
            marginLeft: '5%'
        },
    }

export default CourtsManagement