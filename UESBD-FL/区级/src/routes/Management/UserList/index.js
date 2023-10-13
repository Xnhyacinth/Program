import React from 'react'
import {Card, Button, Table, Modal, Badge} from 'antd'
import axios from 'axios'
import CustomBreadcrumb from '../../../components/CustomBreadcrumb/index'
import '../UserList/style.css'


class UserList extends React.Component {
    state = {
        userInfo: [],
    }


    //加载数据
    loadData = () => {
        var data
        var usersInfo = []
        axios.get('http://localhost:7777/allusers')
            .then(function (response) {
                console.log("数据加载完成")
                data = response.data
                for (var i = 0; i < data.length; i++) {
                    usersInfo.push({
                        index: i + 1,
                        userID: data[i].UserID,
                        userArea: data[i].District,
                        userCourts: data[i].CourtsID,
                        detectionResult: data[i].DetectionHistory[data[i].DetectionHistory.length - 1].Result,
                        detectionDate: data[i].DetectionHistory[data[i].DetectionHistory.length - 1].DetectionDate,
                        detectionDetail: data[i].DetectionHistory
                    })
                }
            })
            .then(() => {
                console.log(usersInfo)
                this.setState({
                    userInfo: usersInfo,
                })
            })
            .catch(function (error) {
                console.log(error);
            });
    }

    componentDidMount() {
        this.loadData()
    }

    expandedRowRender = (record) => {
        console.log(record.index)
        const columns = [
            {
                title: '序号',
                dataIndex: 'index',
                align: 'center',
                width: '10%'
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
                        text === "正常" ? <Badge status='success' text='正常'/> : <Badge status='error' text='窃电'/>
                    );
                },
                align: "center"
            },
        ];

        var data = []
        for (var i = 0; i < this.state.userInfo[record.index - 1].detectionDetail.length; i++) {
            data.push({
                index: i + 1,
                detectionDate: this.state.userInfo[record.index - 1].detectionDetail[i].DetectionDate,
                detectionResult: this.state.userInfo[record.index - 1].detectionDetail[i].Result
            })
        }

        return <Table columns={columns} dataSource={data} pagination={false} bordered={false}/>;
    };

    //用户信息列表项
    tableColumns = [
        {
            title: '序号',
            dataIndex: 'index',
            width: '10%',
            editable: true,
            align: "center"
        },
        {
            title: '用户编号',
            dataIndex: 'userID',
            width: '25%',
            editable: true,
            align: "center"
        },
        {
            title: '所属市/区',
            dataIndex: 'userArea',
            width: '20%',
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
            title: '最近检测结果',
            dataIndex: 'detectionResult',
            width: '20%',
            editable: true,
            render: (text) => {
                return (
                    text === "正常" ? <Badge status='success' text='正常'/> : <Badge status='error' text='窃电'/>
                );
            },
            align: "center"
        },
        {
            title: '最近检测日期',
            dataIndex: 'detectionDate',
            width: '20%',
            editable: true,
            align: "center"
        },
    ]


    render() {
        return (
            <div>
                <CustomBreadcrumb arr={['信息管理', '用户信息管理', '用户列表']}/>
                <Card bordered={false} title='用户列表' style={{marginBottom: 10, minHeight: 440}} align='center'>
                    <Table bordered={false} style={styles.tableStyle} dataSource={this.state.userInfo}
                           columns={this.tableColumns} expandedRowRender={this.expandedRowRender}/>
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


export default UserList