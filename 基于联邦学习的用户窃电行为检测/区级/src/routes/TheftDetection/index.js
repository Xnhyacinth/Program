import React from 'react'
import {Card, Button, Table, BackTop, Badge, notification, Upload, Steps, message} from 'antd'
import axios from 'axios'
import CustomBreadcrumb from '../../components/CustomBreadcrumb/index'
import '../TheftDetection/style.css'

const {Step} = Steps;

//消息框处理函数
const openNotification = Message => {
    notification.info({
        message: Message, duration: 2, placement: `topRight`
    });
};
const props = {
    name: 'file',
    action: 'http://127.0.0.1:5000/upload',
    headers: {
        authorization: 'authorization-text',
    },
};

class TheftDetection extends React.Component {
    state = {
        detectionResult: [],
        checkFile: false,
        detectFinish: false,
        currentStep: 0,
        detectDisabled: true,
        detectResult: null,
    }

    //窃电检测结果展示列表项
    tableColumns = [{
        title: '序号', dataIndex: 'index', width: '8%', align: 'center'
    }, {
        title: '用户编号', dataIndex: 'userID', width: '15%', align: 'center'
    }, {
        title: '所属市/区', dataIndex: 'userArea', width: '15%', align: 'center'
    }, {
        title: '所属台区编号', dataIndex: 'userCourts', width: '15%', align: 'center'
    }, {
        title: '检测日期', dataIndex: 'detectionDate', width: '24%', align: 'center'
    }, {
        title: '检测结果', dataIndex: 'detectionResult', width: '14%', align: 'center', render: (text) => {
            return (text === "正常" ? <Badge status='success' text='正常'/> : <Badge status='error' text='窃电'/>);
        },
    },]

    //点击开始检测按钮处理函数
    theftDetection = () => {
        var url = 'http://127.0.0.1:5000/predict';//传值的地址
        var staticData = []
        fetch(url, {
            method: 'post',//post方法
            headers: {
                "Content-Type": "prediction/json;charset=utf-8",
                'Token': localStorage.getItem('token')
            },
        }).then(res => res.json())
            .catch(error => console.error('Error:', error))
            .then(response => {
                console.log('Success:', response);
                let i = 1
                response.result.forEach(function (e) {
                    staticData.push({
                        index: i,
                        userID: e.user_id,
                        userArea: e.user_area,
                        userCourts: e.user_court,
                        detectionDate: e.date,
                        detectionResult: e.result
                    })
                    axios.post('http://localhost:7777/adddetectionrecord?userID=' + e.user_id, {
                        DetectionDate: e.date,
                        Result: e.result
                    })
                    i += 1
                })
                this.setState({
                    detectResult: response
                })
                //完成检测后弹出消息框
                openNotification("检测完成");
            });

        //设置状态渲染表格数据
        this.setState({
            detectionResult: staticData, currentStep: 2
        })
    }
    handleChange = info => {
        if (info.file.status !== 'uploading') {
            console.log(info.file, info.fileList);
        }
        if (info.file.status === 'done') {
            message.success(`${info.file.name} file uploaded successfully`);
            this.setState({currentStep: 1, detectDisabled: false});
        } else if (info.file.status === 'error') {
            message.error(`${info.file.name} file upload failed.`);
        }
    }

    //页面渲染返回
    render() {
        return (<div style={{height: '750px'}}>
            <CustomBreadcrumb arr={['窃电检测']}/>

            <div style={{height: '15%'}}>
                <Steps current={this.state.currentStep} style={{width: '90%', marginLeft: '5%', marginTop: '5%'}}>
                    <Step title="上传文件" description="上传用户用电数据"/>
                    <Step title="开始检测" description="使用窃电检测模型检测用电数据"/>
                    <Step title="检测完成"/>
                </Steps>
                <div style={{display: 'flex', marginTop: 20}}>
                    <Upload {...props} style={{marginLeft: '125px'}} onChange={this.handleChange}>
                        <Button type='primary'>上传文件</Button>
                    </Upload>
                    <Button type='primary' onClick={this.theftDetection} disabled={this.state.detectDisabled}
                            style={{marginLeft: '625px'}}>开始检测</Button>
                </div>
            </div>
            <div>
                <Card bordered={false} title='' style={{marginBottom: 10, minHeight: 300}} align='center'>

                    <Table style={styles.tableStyle} bordered='true' dataSource={this.state.detectionResult}
                           columns={this.tableColumns}/>
                </Card>
            </div>
        </div>)
    }
}

const styles = {
    tableStyle: {
        width: '90%',
    },
}


export default TheftDetection