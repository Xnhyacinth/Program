import React, { useState } from 'react'
import {
    Card,
    Button,
    Table,
    Badge,
    Steps,
    Input,
    InputNumber,
    Radio,
    Select
} from 'antd'
import axios from 'axios'
import CustomBreadcrumb from '../../components/CustomBreadcrumb/index'
import TextArea from "antd/es/input/TextArea";
import '../StartTraining/style.css'

const data = [];
const { Step } = Steps;
const { Option } = Select


data.push({
    key: 1,
    courtsId: "C001",
    courtsArea: "北京市昌平区",
    courtsContribution: 40.24,
    courtsUserNum: 16135,
    courtsStatus: '在线',
    courtsEpsilon: 25
})
data.push({
    key: 2,
    courtsId: "C002",
    courtsArea: "北京市海淀区",
    courtsContribution: 40.04,
    courtsUserNum: 14000,
    courtsStatus: '在线',
    courtsEpsilon: 50
})
data.push({
    key: 3,
    courtsId: "C003",
    courtsArea: "北京市房山区",
    courtsContribution: 39.68,
    courtsUserNum: 8000,
    courtsStatus: '在线',
    courtsEpsilon: 10
})


class StartTraining extends React.Component {
    state = {
        loading: false,
        data,
        selectedRowKeys: [], // Check here to configure the default column
        startDisabled: true, //控制开始训练按钮是否可按
        confirmDisabled: true, //控制确认按钮是否可按
        ifDP: false,
        ifAsycn: false,
        currentStep: 0,
        train_result: null,
    }

    tableColumns = [
        {
            title: '序号',
            dataIndex: 'key',
            width: '5%',
            align: 'center'
        },
        {
            title: '台区编号',
            dataIndex: 'courtsId',
            editable: true,
            align: 'center'
        },
        {
            title: '所属市/区',
            dataIndex: 'courtsArea',
            editable: true,
            align: 'center'
        },
        {
            title: '历史贡献度',
            dataIndex: 'courtsContribution',
            editable: true,
            align: 'center'
        },
        {
            title: '用户数量',
            dataIndex: 'courtsUserNum',
            editable: true,
            align: 'center'
        },
        {
            title: '台区状态',
            dataIndex: 'courtsStatus',
            render: (text, record) => {
                return <div>
                    {text === "在线" ? <Badge status="success" text="在线" /> : <Badge status="default" text="离线" />}
                </div>
            },
            align: 'center'
        },
        {
            title: '隐私预算',
            dataIndex: 'courtsEpsilon',
            editable: true,
            align: 'center'
        },
    ]

    //点击提交按钮
    submitDescription = () => {
        if (this.state.ifAsycn == true) {
            this.setState({
                currentStep: 2,
                startDisabled: false
            })
        }
        else {
            this.setState({
                currentStep: 1,
                confirmDisabled: false
            })
        }

    }

    //选择台区后点击确认按钮
    confirmCourts = () => {
        this.setState({
            currentStep: 2,
            startDisabled: false
        })
    }

    //点击开始训练按钮响应函数
    startTraining = () => {
        console.log("开始训练")
        this.submit_train();
    }

    //是否引入差分隐私单选框改变响应函数
    selectDP = (e) => {
        console.log('radio checked', e.target.value);
        this.setState({
            ifDP: e.target.value,
        });
    };

    //选择同步和异步聚合算法
    handleChange = e => {
        if (e == "Asycn") {
            this.setState({
                ifAsycn: true
            })
        }
        else {
            this.setState({
                ifAsycn: false
            })
        }
    }

    reset = () => {
        this.setState({ loading: true });
        // ajax request after empty completing
        setTimeout(() => {
            this.setState({
                selectedRowKeys: [],
                loading: false,
            });
        }, 50);
    };
    onSelectChange = selectedRowKeys => {
        console.log('selectedRowKeys changed: ', selectedRowKeys);
        this.setState({ selectedRowKeys });
    };

    submit_train() {
        const lr = document.querySelectorAll('.lr')[0].value;
        const num_comm = document.querySelectorAll('.num')[0].value;
        const aggregation = document.querySelectorAll('.aggregation')[0].value;
        const optimizer = document.querySelectorAll('.optimizer')[0].value;
        const isDP = document.getElementsByName('dp')[0].checked;
        console.log(lr, num_comm, aggregation, optimizer, isDP);
        let e = 0;
        if (isDP) {
            e = document.querySelectorAll('.e')[0].value;
            console.log(e);
        }
        var url = 'http://127.0.0.1:5000/start';//传值的地址
        var data = {
            "lr": lr,
            "num_comm": num_comm,
            "aggregation": aggregation,
            "optimizer": optimizer,
            "isDP": isDP,
            "e": e
        };//传值的内容，键:值格式
        console.log(data);
        fetch(url, {
            method: 'post',//post方法
            headers: {
                "Content-Type": "application/json;charset=utf-8",
                'Token': localStorage.getItem('token')
            },
            body: JSON.stringify(data)//转为json格式
        }).then(res => res.json())
            .catch(error => console.error('Error:', error))
            .then(response => {
                console.log('Success:', response);
                this.setState({
                    train_result: response,
                    currentStep: 3,
                })
            });
        console.log('--------' + this.state.train_result);
    };

    render() {
        // eslint-disable-next-line no-unused-vars
        const { loading, selectedRowKeys } = this.state;
        const rowSelection = {
            selectedRowKeys,
            onChange: this.onSelectChange,
        };
        const hasSelected = selectedRowKeys.length > 0;
        return (
            <div>
                <CustomBreadcrumb arr={['启动训练']} />

                <div style={{ height: '335px', width: '100%' }}>
                    <div style={{ height: '120px', paddingTop: '40px' }}>
                        <Steps current={this.state.currentStep} style={{ width: '90%', marginLeft: '5%' }}>
                            <Step title="填写信息" description="根据提示填写联邦学习训练任务信息" />
                            <Step title="选择台区" description="选择参与联邦学习训练的台区" />
                            <Step title="开始训练" />
                            <Step title="训练完成" />
                        </Steps>
                    </div>
                    <div style={{ height: '30px' }}>
                        <Button type='primary' style={{ marginBottom: 5, marginLeft: '63%' }} size='small'
                            disabled={this.state.startDisabled} onClick={this.startTraining}>开始训练</Button>
                    </div>
                    <div style={{ height: '185px' }}>
                        <div style={{
                            height: '60px',
                            paddingLeft: 32,
                            fontSize: 16,
                            paddingTop: 25,
                            borderBottom: '1px solid #e8e8e8'
                        }}>
                            <text>1.填写信息</text>
                        </div>
                        <div style={{ height: '125px', display: 'flex' }}>
                            <div style={{ width: '50%', height: '100%', display: 'flex' }}>
                                <div style={{ width: '50%', paddingTop: 10, paddingLeft: '2%' }}>
                                    <div>
                                        <text>聚合轮数:</text>
                                        <Input className="num" size='small' style={{ marginLeft: '2%', width: '20%' }}
                                            defaultValue={20} />
                                        <text style={{ marginLeft: '6%' }}>聚合方式:</text>
                                        <Select defaultValue="Sycn" style={{ width: 120 }} onChange={this.handleChange}>
                                            <Option value="Sycn">同步</Option>
                                            <Option value="Asycn">异步</Option>
                                        </Select>
                                    </div>
                                    <div style={{ height: '33%' }}>
                                        <text>聚合算法:</text>
                                        <Input className="aggregation" size='small' style={{ marginLeft: '2%', width: '20%' }}
                                            defaultValue={"FedAvg"} />

                                        <text style={{ marginLeft: '6%' }}>优化算法:</text>
                                        <Input className="optimizer" size='small' style={{ marginLeft: '2%', width: '20%', marginTop: '2%' }}
                                            defaultValue={"RAdam"} />

                                    </div>
                                    <div style={{ height: '33%' }}>
                                        <text > 学 习 率:</text>
                                        <Input className="lr" size='small' style={{ marginLeft: '3%', width: '15%' }}
                                            defaultValue={0.001} />
                                        <text style={{ marginLeft: '3%' }}>引入差分隐私:</text>
                                        <Radio.Group name="dp" onChange={this.selectDP}
                                            style={{ marginLeft: '1%', width: '37%' }}
                                            defaultValue={false}>
                                            <Radio value={true}>是</Radio>
                                            <Radio value={false}>否</Radio>
                                        </Radio.Group>
                                    </div>
                                    {/*<div style={{height: '33%', width: '20%'}}>*/}
                                    {/*<text>聚合轮数:</text>*/}
                                    {/*<Input className="num" style={{marginLeft: '10%'}}*/}
                                    {/*       defaultValue={20}/>*/}
                                    {/*<text style={{marginLeft: '20%'}}>聚合算法:</text>*/}
                                    {/*<Input className="aggregation" style={{marginLeft: 10, width: '20%'}}*/}
                                    {/*       defaultValue={"FedAvg"}/>*/}
                                    {/*</div>*/}
                                    {/*<div style={{height: '33%'}}>*/}
                                    {/*    <text>优化算法:</text>*/}
                                    {/*    <Input className="optimizer" style={{marginLeft: 10, width: '90px'}}*/}
                                    {/*           defaultValue={"RAdam"}/>*/}
                                    {/*    <text style={{marginLeft: 45}}>学习率:</text>*/}
                                    {/*    <Input className="lr" style={{marginLeft: 10, width: '90px'}}*/}
                                    {/*           defaultValue={0.001}/>*/}
                                    {/*</div>*/}
                                    {/*<div style={{height: '33%'}}>*/}
                                    {/*    <text>引入差分隐私:</text>*/}
                                    {/*    <Radio.Group name="dp" onChange={this.selectDP} style={{marginLeft: 10}}*/}
                                    {/*                 defaultValue={false}>*/}
                                    {/*        <Radio value={true}>是</Radio>*/}
                                    {/*        <Radio value={false}>否</Radio>*/}
                                    {/*    </Radio.Group>*/}
                                    {/*    <text>隐私预算:</text>*/}
                                    {/*    <Input className="e" style={{marginLeft: 10, width: '75px'}}*/}
                                    {/*           disabled={!this.state.ifDP} defaultValue={25}/>*/}
                                    {/*</div>*/}
                                </div>
                                <div style={{ width: '50%', paddingTop: 10, paddingLeft: '5%' }}>
                                    <text>任务描述:</text>
                                    <TextArea rows={2} placeholder='请对训练任务进行简要描述' />
                                    <Button type='primary' size='small' style={{ marginTop: '5%', marginLeft: '80%' }}
                                        onClick={this.submitDescription}>提交</Button>
                                </div>
                            </div>
                            <div style={{
                                width: '55%',
                                height: '100%',
                                paddingTop: 10,
                                paddingLeft: '2%',
                                paddingRight: 20
                            }}>
                                <div style={{
                                    width: '100%',
                                    height: '100%',
                                    border: '2px solid #d9d9d9',
                                    borderRadius: '10px',
                                    padding: '5px 10px 5px 10px'
                                }}>
                                    <div style={{ height: '20%', fontSize: 15 }}>#信息填写说明</div>
                                    <div style={{ fontSize: 14, marginTop: 3, display: 'flex' }}>
                                        <div style={{ marginLeft: '2%', width: '33%' }}>
                                            1.轮数：联邦学习中服务器聚合模型次数
                                        </div>
                                        <div style={{ marginLeft: '2%', width: '33%' }}>
                                            2.聚合方式：异步聚合无需选择台区
                                        </div>
                                        <div style={{ marginLeft: '2%', width: '33%' }}>
                                            3.聚合算法：聚合过程中使用的聚合算法
                                            
                                        </div>
                                    </div>
                                    <div style={{ fontSize: 14, marginTop: 3, display: 'flex' }}>
                                        <div style={{ marginLeft: 10, width: '50%' }}>
                                            4.优化算法：模型迭代过程使用的优化器
                                            
                                        </div>
                                        <div style={{ marginLeft: 10 }}>
                                            5.学习率：模型迭代过程中使用的优化器的学习率
                                        </div>
                                    </div>
                                    <div style={{ fontSize: 14, marginTop: 3, display: 'flex' }}>
                                        <div style={{ marginLeft: 10, width: '50%' }}>
                                            6.是否引入差分隐私：训练过程中是否引入差分隐私机制保护梯度
                                        </div>
                                        <div style={{ marginLeft: 10 }}>
                                            7.描述：对训练任务的简要描述
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div style={{ height: '50%' }}>
                    <Card bordered={false} title='2.选择台区'>
                        <div>
                            <div>
                                <Button type="primary" onClick={this.reset} disabled={!hasSelected} loading={loading}
                                    style={{ marginLeft: '5%', marginBottom: 10 }}>
                                    重置
                                </Button>
                                <Button type="primary" onClick={this.confirmCourts}
                                    style={{ marginLeft: 20, marginBottom: 10 }}
                                    disabled={this.state.confirmDisabled}>
                                    确认
                                </Button>
                                <span style={{ marginLeft: 8 }}>
                                    {hasSelected ? `共选择 ${selectedRowKeys.length} 个台区` : ''}
                                </span>
                            </div>
                            <Table rowSelection={rowSelection} style={styles.tableStyle}
                                bordered columns={this.tableColumns} dataSource={data} />
                        </div>
                    </Card>
                </div>
            </div>
        )
    }
}

const styles = {
    tableStyle: {
        width: '90%',
        marginLeft: '5%'
    },
}

export default StartTraining