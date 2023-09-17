import React from 'react'
import { Calendar, Table, Badge, Icon, Divider } from 'antd'
import axios from 'axios'
import ReactEcharts from 'echarts-for-react';
import '../UserPage/style.css'

function getElectricData(value) {
    let ElectricData
    switch (value.date()) {
        case 1:
            ElectricData = 11.78
            break;
        case 2:
            ElectricData = 18.59
            break;
        case 3:
            ElectricData = 26.47
            break;
        case 4:
            ElectricData = 7.6
            break;
        case 5:
            ElectricData = 9.93
            break;
        case 6:
            ElectricData = 14.25
            break;
        case 7:
            ElectricData = 8.12
            break;
        case 8:
            ElectricData = 6.57
            break;
        case 9:
            ElectricData = 28.90
            break;
        case 10:
            ElectricData = 14.80
            break;
        case 11:
            ElectricData = 24.36
            break;
        case 12:
            ElectricData = 5.98
            break;
        case 13:
            ElectricData = 3.67
            break;
        case 14:
            ElectricData = 0.47
            break;
        case 15:
            ElectricData = 8.99
            break;
        case 16:
            ElectricData = 24.56
            break;
        case 17:
            ElectricData = 13.87
            break;
        case 18:
            ElectricData = 19.58
            break;
        case 19:
            ElectricData = 24.87
            break;
        case 20:
            ElectricData = 5.80
            break;
        case 21:
            ElectricData = 2.36
            break;
        case 22:
            ElectricData = 9.88
            break;
        case 23:
            ElectricData = 10.07
            break;
        case 24:
            ElectricData = 12.89
            break;
        case 25:
            ElectricData = 13.78
            break;
        case 26:
            ElectricData = 24.78
            break;
        case 27:
            ElectricData = 22.50
            break;
        case 28:
            ElectricData = 12.38
            break;
        case 29:
            ElectricData = 33.40
            break;
        case 30:
            ElectricData = 14.38
            break;
        default:
    }
    return ElectricData || [];
}

function dateCellRender(value) {
    const ElectricData = getElectricData(value);
    return (
        <ul className="events">
            <li>
                <div style={{ marginLeft: '25%', fontSize: 15 }}>用电量</div>
                <text style={{ marginTop: '5%', marginLeft: '25px', fontSize: 20 }}>{ElectricData}kwh</text>
            </li>
        </ul>
    );
}



class UserPage extends React.Component {

    state = {
        detectionRecord: []
    }

    loadData = () => {
        var data
        var staticData = []
        axios.get('http://localhost:7777/user?userID=U001')
            .then(function (response) {
                console.log("数据加载完成")
                data = response.data.DetectionHistory
                for (var i = 0; i < data.length; i++) {
                    staticData.push({
                        index: i + 1,
                        detectionDate: data[i].DetectionDate,
                        detectionResult: data[i].Result
                    })
                }
            })
            .then(() => {
                this.setState({
                    detectionRecord: staticData
                })
            })
            .catch(function (error) {
                console.log(error);
            });
        
    }

    componentDidMount() {
        this.loadData()
    }


    getOption = () => {
        let option = {
            grid: {
                top: '25%',
                left: '10%',
                right: '8%',
                bottom: '20%'
            },
            xAxis: {
                type: 'category',
                data: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    data: [19.55, 25.9, 24.5, 30.66, 24.89, 26.68, 26.94, 26.86, 27.29, 16.67, 16.14, 26.43, 30.56, 26.21, 29.25, 29.42, 48.65, 50.79, 41.04, 43.81, 33.57, 41.08, 22.63, 23.25, 28.49, 17, 19.02, 27.69, 13.89, 22.87],
                    type: 'line'
                }
            ]
        };
        return option;
    };

    tableColumns = [
        {
            title: '序号',
            dataIndex: 'index',
            align: 'center',
            width: '15%'
        },
        {
            title: '检测日期',
            dataIndex: 'detectionDate',
            align: 'center'
        },
        {
            title: '检测结果',
            dataIndex: 'detectionResult',
            render: (text) => {
                return (
                    text === "正常" ? <Badge status='success' text='正常' /> : <Badge status='error' text='窃电' />
                );
            },
            align: "center"
        },
    ]

    render() {
        return (
            <div style={{ height: '815px', width: '100%', paddingLeft: '3%', paddingRight: '3%', paddingTop: '1%', paddingBottom: '2%', display: 'flex' }}>
                <div style={{ height: '100%', width: '60%' }}>
                    <div style={{ height: '100%', marginRight: '40px' }}><Calendar style={{ height: '100%' }} dateCellRender={dateCellRender} /></div>
                </div>
                <div style={{ height: '100%', width: '40%' }}>
                    <div style={{ height: '20%', border: '3px solid #55B4AE', borderRadius: 10, display: 'flex' }}>
                        <div style={{ height: '100%', width: '25%', paddingTop: 30, paddingBottom: 30, paddingLeft: 20, paddingRight: 20 }}>
                            <div style={{ border: '2px solid #bfbfbf', height: '100%', paddingLeft: 10, paddingRight: 10, paddingTop: 10, paddingBottom: 10 }}>
                                <div style={{ height: '40%' }}><text>用户编号</text></div>
                                <div style={{ height: '60%', fontSize: 30 }}><Icon type="user" /><text style={{ marginLeft: 5 }}>U001</text></div>
                            </div>
                        </div>
                        <div style={{ height: '100%', width: '25%', paddingTop: 30, paddingBottom: 30, paddingLeft: 20, paddingRight: 20 }}>
                            <div style={{ border: '2px solid #bfbfbf', height: '100%', paddingLeft: 10, paddingRight: 10, paddingTop: 10, paddingBottom: 10 }}>
                                <div style={{ height: '40%' }}><text>台区编号</text></div>
                                <div style={{ height: '60%', fontSize: 30 }}><Icon type="schedule" /><text style={{ marginLeft: 5 }}>C001</text></div>
                            </div>
                        </div>
                        <div style={{ height: '100%', width: '25%', paddingTop: 30, paddingBottom: 30, paddingLeft: 20, paddingRight: 20 }}>
                            <div style={{ border: '2px solid #bfbfbf', height: '100%', paddingLeft: 10, paddingRight: 10, paddingTop: 10, paddingBottom: 10 }}>
                                <div style={{ height: '40%' }}><text>最近检测日期</text></div>
                                <div style={{ height: '60%', fontSize: 30 }}><Icon type="calendar" /><text style={{ 'font-size': 15, marginLeft: 5 }}>2022-5-12</text></div>
                            </div>
                        </div>
                        <div style={{ height: '100%', width: '25%', paddingTop: 30, paddingBottom: 30, paddingLeft: 20, paddingRight: 20 }}>
                            <div style={{ border: '2px solid #bfbfbf', height: '100%', paddingLeft: 10, paddingRight: 10, paddingTop: 10, paddingBottom: 10 }}>
                                <div style={{ height: '40%' }}><text>检测结果</text></div>
                                <div style={{ height: '60%', fontSize: 30 }}><text style={{ color: 'green', marginLeft: '20%' }}>正常</text></div>
                            </div>
                        </div>

                    </div>
                    <div style={{ height: '80%', marginTop: '30px', padding: '20, 20, 20, 20' }}>
                        <div style={{ height: '100%', width: '100%', border: '3px solid #55B4AE', borderRadius: 10 }}>
                            <div style={{ height: '45%' }}>
                                <div style={{ height: '5%', width: '100%' }}>
                                    <Divider style={{ width: '80%', marginLeft: '10%', fontSize: 20 }}>窃电检测历史</Divider>
                                </div>
                                <div style={{ height: '95%', width: '100%' }}>
                                    <Table style={{ width: '80%', marginLeft: '10%', marginTop: '5%', maxHeight: '80%' }} columns={this.tableColumns} dataSource={this.state.detectionRecord}></Table>
                                </div>
                            </div>
                            <div style={{ height: '45%' }}>
                                <div style={{ height: '5%', width: '100%' }}>
                                    <Divider style={{ width: '80%', marginLeft: '10%', fontSize: 20 }}>近30天用电趋势</Divider>
                                </div>
                                <div style={{ height: '95%', width: '100%' }}>
                                    <ReactEcharts option={this.getOption()} />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}


export default UserPage