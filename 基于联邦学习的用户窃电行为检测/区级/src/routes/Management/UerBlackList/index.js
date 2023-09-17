import React from 'react'
import { Card, Button, Table, BackTop, Badge, Tag, Icon, Col } from 'antd'
import 'antd/dist/antd.css';
import axios from 'axios'
import CustomBreadcrumb from '../../../components/CustomBreadcrumb/index'
import ReactEcharts from 'echarts-for-react'
import '../UerBlackList/style.css'


class UserList extends React.Component {
    state = {
        userInfo: [],
    }

    lightWarning = 0
    moderateWarning = 0
    seriousWarning = 0

    //设置饼图配置项
    getOption = () => {
        return {
            tooltip: {
                trigger: 'item'
            },
            series: [
                {
                    name: '用户预警等级',
                    type: 'pie',
                    radius: '30%',
                    center: ['50%', '25%'],
                    data: [
                        { value: this.lightWarning, name: '轻度警告' },
                        { value: this.moderateWarning, name: '中度警告' },
                        { value: this.seriousWarning, name: '重度警告' },
                    ],
                    color: ['#fadb14', '#fa8c16', '#f5222d'],
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        }
    }

    //加载数据
    loadData = () => {
        var data
        var staticData = []
        axios.get('http://localhost:7777/allusers')
            .then(function (response) {
                console.log("数据加载完成")
                data = response.data
                var index = 1
                for (var i = 0; i < data.length; i++) {
                    if (data[i].Reputation > 0) {
                        staticData.push({
                            index: index,
                            userID: data[i].UserID,
                            userArea: data[i].District,
                            userCourts: data[i].CourtsID,
                            theftCount: data[i].Reputation,
                            detectionResult: data[i].DetectionHistory[data[i].DetectionHistory.length - 1].Result,
                            detectionDate: data[i].DetectionHistory[data[i].DetectionHistory.length - 1].DetectionDate,
                            detectionDetail: data[i].DetectionHistory
                        })
                        index++
                    }
                }
            })
            .then(() => {
                for (var i = 0; i < staticData.length; i++) {
                    if (staticData[i].theftCount < 5) {
                        this.lightWarning += 1
                    }
                    else if (5 <= staticData[i].theftCount && staticData[i].theftCount <= 9) {
                        this.moderateWarning += 1
                    }
                    else if (staticData[i].theftCount > 9) {
                        this.seriousWarning += 1
                    }
                }
                this.setState({
                    userInfo: staticData,
                })
            })
            .catch(function (error) {
                console.log(error);
            });

        

        /*this.setState({
            userInfo: staticData,
        })*/
    }

    componentDidMount() {
        this.loadData()
    }

    //用户信息列表项
    tableColumns = [
        {
            title: '序号',
            dataIndex: 'index',
            width: '8%',
            editable: true,
            align: "center"
        },
        {
            title: '用户编号',
            dataIndex: 'userID',
            width: '15%',
            editable: true,
            align: "center"
        },
        {
            title: '所属市/区',
            dataIndex: 'userArea',
            width: '15%',
            editable: true,
            align: "center"
        },
        {
            title: '所属台区编号',
            dataIndex: 'userCourts',
            width: '15%',
            editable: true,
            align: "center"
        },
        {
            title: '累计窃电次数',
            dataIndex: 'theftCount',
            width: '12%',
            editable: true,
            align: "center"
        },
        {
            title: '警告级别',
            dataIndex: 'theftCount',
            width: '12%',
            editable: true,
            render: (text) => {
                if (text < 5 && text > 0) {
                    return <Tag color='yellow'><Icon type="warning" />轻度警告</Tag>
                }
                else if (5 <= text && text <= 9) {
                    return <Tag color='orange'><Icon type="warning" />中度警告</Tag>
                }
                else if (text > 9) {
                    return <Tag color='#cd201f'><Icon type="warning" />重度警告</Tag>
                }
            },
            align: "center"
        },
        {
            title: '最近检测结果',
            dataIndex: 'detectionResult',
            width: '12%',
            editable: true,
            render: (text) => {
                return (
                    text === "正常" ? <Badge status='success' text='正常' /> : <Badge status='error' text='窃电' />
                );
            },
            align: "center"
        },
        {
            title: '最近检测日期',
            dataIndex: 'detectionDate',
            width: '18%',
            editable: true,
            align: "center"
        },
        /*{
            title: '操作',
            dataIndex: 'index',
            render: (record) => {
                return <Button type='danger' onClick={() => this.WarnUser(record)}>警告</Button>
            },
            align: "center"
        },*/
    ]

    render() {

        return (
            <div style={{ height: '100%', width: '100%' }}>

                <CustomBreadcrumb arr={['信息管理', '用户信息管理', '用户黑名单']} />

                <div style={{ height: '200px', display: 'flex', paddingLeft: '7%', paddingBottom: '30px', paddingTop: '30px', paddingRight: '7%' }}>
                    <div style={{ height: '100%', width: '25%', padding: '10px 10px 10px 10px' }}>
                        <div style={{ height: '100%', border: '2px solid #fadb14', 'border-radius': '10px', paddingLeft: '20px', paddingRight: '20px', paddingTop: 5 }}>
                            <div style={{ height: '40%', borderBottom: '2px solid #fadb14', fontSize: 20 }}>
                                <text style={{ marginLeft: '20%' }}>轻度警告用户数量</text>
                            </div>
                            <div style={{ height: '60%', fontSize: 40 }}>
                                <text style={{ marginLeft: '45%' }}>{this.lightWarning}</text>
                            </div>
                        </div>
                    </div>
                    <div style={{ height: '100%', width: '25%', padding: '10px 10px 10px 10px' }}>
                        <div style={{ height: '100%', border: '2px solid #fa8c16', 'border-radius': '10px', paddingLeft: '20px', paddingRight: '20px', paddingTop: 5 }}>
                            <div style={{ height: '40%', borderBottom: '2px solid #fa8c16', fontSize: 20 }}>
                                <text style={{ marginLeft: '20%' }}>中度警告用户数量</text>
                            </div>
                            <div style={{ height: '60%', fontSize: 40 }}>
                                <text style={{ marginLeft: '45%' }}>{this.moderateWarning}</text>
                            </div>
                        </div>
                    </div>
                    <div style={{ height: '100%', width: '25%', padding: '10px 10px 10px 10px', fontSize: 20 }}>
                        <div style={{ height: '100%', border: '2px solid #f5222d', 'border-radius': '10px', paddingLeft: '20px', paddingRight: '20px', paddingTop: 5 }}>
                            <div style={{ height: '40%', borderBottom: '2px solid #f5222d' }}>
                                <text style={{ marginLeft: '20%' }}>重度警告用户数量</text>
                            </div>
                            <div style={{ height: '60%', fontSize: 40 }}>
                                <text style={{ marginLeft: '45%' }}>{this.seriousWarning}</text>
                            </div>
                        </div>
                    </div>
                    <div style={{ height: '100%', width: '25%' }}>
                        <ReactEcharts option={this.getOption()}></ReactEcharts>
                    </div>
                </div>

                <div style={{ 'padding-right': '50px', 'padding-left': '50px', height: '75%', width: '100%', }}>
                    <div style={{ height: '20%', borderTop: '2px solid #bfbfbf', width: '100%', fontSize: 30, fontFamily: '' }}>
                        <text style={{ marginLeft: '45%' }}>用户黑名单</text>
                    </div>
                    <Table style={styles.tableStyle} bordered dataSource={this.state.userInfo}
                        columns={this.tableColumns} />
                </div>

            </div >
        )
    }
}

const styles = {
    tableStyle: {
        width: '90%',
        marginLeft: '5%',
        marginTop: '1%'
    },
}


export default UserList