import React, {useState} from 'react'
import {
    Card,
    Button,
    Table,
    Cascader,
    BackTop,
    Form,
    InputNumber,
    Input
} from 'antd'
import axios from 'axios'
import CustomBreadcrumb from '../../../components/CustomBreadcrumb/index'
import TextArea from "antd/es/input/TextArea";

const data = [];

data.push({
    key:1,
    id:"C001",
    area_id:"北京市昌平区",
    contribution:40.24,
    user_num:16135
})
data.push({
    key:2,
    id:"C002",
    area_id:"北京市海淀区",
    contribution:40.04,
    user_num:14000
})
data.push({
    key:3,
    id:"C003",
    area_id:"北京市房山区",
    contribution:39.68,
    user_num:8000
})
// const  { TextArea }  = this.getInput();
const FormItem = Form.Item;
const EditableContext = React.createContext();
const EditableRow = ({form, index, ...props}) => (
    <EditableContext.Provider value={form}>
        <tr {...props} />
    </EditableContext.Provider>
);
const EditableFormRow = Form.create()(EditableRow);

class EditableCell extends React.Component {
    getInput = () => {
        if (this.props.inputType === 'number') {
            return <InputNumber/>;
        }
        return <Input/>;
    };

    render() {
        const {
            editing,
            dataIndex,
            title,
            inputType,
            record,
            index,
            ...restProps
        } = this.props;
        return (
            <EditableContext.Consumer>
                {(form) => {
                    const {getFieldDecorator} = form;
                    return (
                        <td {...restProps}>
                            {editing ? (
                                <FormItem style={{margin: 0}}>
                                    {getFieldDecorator(dataIndex, {
                                        rules: [{
                                            required: true,
                                            message: `Please Input ${title}!`,
                                        }],
                                        initialValue: record[dataIndex],
                                    })(this.getInput())}
                                </FormItem>
                            ) : restProps.children}
                        </td>
                    );
                }}
            </EditableContext.Consumer>
        );
    }
}

class TableDemo extends React.Component {
    state = {
        filteredInfo: null,
        sortedInfo: null,
        loading: false,
        data4: [],
        pagination: {
            pageSize: 8
        },
        data,
        editingKey: '',
        selectedRowKeys: [], // Check here to configure the default column
    }

    componentDidMount() {
        this.getRemoteData()
    }

    columns = [
        {
            title: '台区编号',
            dataIndex: 'id',
            width: '10',
            editable: true,
        },
        {
            title: '所属市/区',
            dataIndex: 'area_id',
            width: '10',
            editable: true,
        },
        {
            title: '历史贡献度',
            dataIndex: 'contribution',
            width: '10',
            editable: true,
        },
        {
            title: '用户数量',
            dataIndex: 'user_num',
            width: '10',
            editable: true,
        },
    ]


    handleChange = (pagination, filters, sorter) => {
        this.setState({
            filteredInfo: filters,
            sortedInfo: sorter,
        })
    }
    clearFilters = () => {
        this.setState({filteredInfo: null})
    }
    clearAll = () => {
        this.setState({
            filteredInfo: null,
            sortedInfo: null,
        })
    }
    setSort = (type) => {
        this.setState({
            sortedInfo: {
                order: 'descend',
                columnKey: type,
            },
        })
    }

    getRemoteData(params) {
        this.setState({
            loading: true
        })
        axios.get('https://randomuser.me/api', {
            params: {
                results: 10,
                size: 200,
                ...params
            }
        }).then(res => {
            const pagination = {...this.state.pagination};
            pagination.total = 200
            this.setState({
                loading: false,
                data4: res.data.results,
                pagination
            })
        })
    }

    handleTableChange = (pagination, filters, sorter) => {
        const pager = {...this.state.pagination};
        pager.current = pagination.current;
        this.setState({
            pagination: pager,
        });
        this.getRemoteData({
            results: pagination.pageSize,
            page: pagination.current,
            sortField: sorter.field,
            sortOrder: sorter.order,
            ...filters,
        })
    }
    onDelete = (key) => {
        const arr = this.state.data.slice()
        this.setState({
            data: arr.filter(item => item.key !== key)
        })
    }
    handleAdd = () => {
        const {data7, count} = this.state //本来想用data7的length来代替count，但是删除行后，length会-1
        const newData = {
            key: count,
            name: `Edward King ${count}`,
            age: 32,
            address: `London, Park Lane no. ${count}`,
        };
        this.setState({
            data7: [...data7, newData],
            count: count + 1
        })
    }
    isEditing = (record) => {
        return record.key === this.state.editingKey;
    };

    edit(key) {
        this.setState({editingKey: key});
    }

    save(form, key) {
        form.validateFields((error, row) => {
            if (error) {
                return;
            }
            const newData = [...this.state.data];
            const index = newData.findIndex(item => key === item.key);
            if (index > -1) {
                const item = newData[index];
                newData.splice(index, 1, {
                    ...item,
                    ...row,
                });
                this.setState({data: newData, editingKey: ''});
            } else {
                newData.push(data);
                this.setState({data: newData, editingKey: ''});
            }
        });
    }

    cancel = () => {
        this.setState({editingKey: ''});
    };

    start = () => {
        this.setState({loading: true});
        // ajax request after empty completing
        setTimeout(() => {
            this.setState({
                selectedRowKeys: [],
                loading: false,
            });
        }, 1000);
    };
    onSelectChange = selectedRowKeys => {
        console.log('selectedRowKeys changed: ', selectedRowKeys);
        this.setState({selectedRowKeys});
    };

    render() {
        // eslint-disable-next-line no-unused-vars
        let {sortedInfo, filteredInfo} = this.state
        sortedInfo = sortedInfo || {}
        filteredInfo = filteredInfo || {}
        const components = {
            body: {
                row: EditableFormRow,
                cell: EditableCell,
            },
        };
        const columns = this.columns.map((col) => {
            if (!col.editable) {
                return col;
            }
            return {
                ...col,
                onCell: record => ({
                    record,
                    inputType: col.dataIndex === 'age' ? 'number' : 'text',
                    dataIndex: col.dataIndex,
                    title: col.title,
                    editing: this.isEditing(record),
                }),
            };
        });
        const {loading, selectedRowKeys} = this.state;
        const rowSelection = {
            selectedRowKeys,
            onChange: this.onSelectChange,
        };
        const hasSelected = selectedRowKeys.length > 0;
        return (
            <div>
                <CustomBreadcrumb arr={['启动训练']}/>

                <Card bordered={false} title='任务信息' style={{marginBottom: 10, minHeight: 200}} id='editTable'>
                    <p>
                        {/* <Button   style={{margin: 10}} type="primary" onClick={this.handleAdd}>查询当前在线台区</Button>
            <Badge status="success" text="当前在线设备数量为55个" /> */}
                        轮数：
                        <InputNumber
                            addonBefore={<Cascader placeholder="cascader" style={{width: 150}}/>}
                            defaultValue={0}
                        />
                        <Button type="primary" style={{float: "right", marginRight: 800}}
                                onClick={this.handleAdd}>开始训练</Button>
                    </p>
                    <p>
                        任务描述
                    </p>
                    <TextArea rows={4} style={{width: '40%', height: 150, margin: 10}} placeholder="任务描述信息"
                              autosize={{minRows: 7, maxRows: 7}}/>
                    {/*<Divider/>*/}
                    {/*<TextArea rows={4} placeholder="maxLength is 6" maxLength={6} />*/}

                </Card>
                <Card bordered={false} title='台区信息' style={{marginBottom: 10, minHeight: 300}} id='editTable'>
                    {/*<Table style={styles.tableStyle} components={components} bordered*/}
                    {/*       dataSource={this.state.data}*/}
                    {/*       columns={columns}/>*/}
                    <div>
                        <div style={{marginBottom: 16}}>
                            <Button type="primary" onClick={this.start} disabled={!hasSelected} loading={loading}>
                                重置
                            </Button>
                            <span style={{marginLeft: 8}}>
                            {hasSelected ? `共选择 ${selectedRowKeys.length} 个台区` : ''}
                            </span>
                        </div>
                        <Table rowSelection={rowSelection} components={components} style={styles.tableStyle}
                               bordered columns={columns} dataSource={data}/>
                        <p>
                            共有{data.length}个台区
                        </p>
                    </div>
                </Card>
                <BackTop visibilityHeight={200} style={{right: 50}}/>
                {/* <Affix style={styles.affixBox}>
          <Anchor offsetTop={50} affix={false}>
            <Anchor.Link href='#howUse' title='何时使用'/>
            <Anchor.Link href='#basicUsage' title='基本用法'/>
            <Anchor.Link href='#select' title='可选择'/>
            <Anchor.Link href='#filterOrSort' title='排序和筛选'/>
            <Anchor.Link href='#remoteLoading' title='远程加载数据'/>
            <Anchor.Link href='#unfold' title='可展开'/>
            <Anchor.Link href='#fixed' title='固定头和列'/>
            <Anchor.Link href='#editTable' title='可编辑的表格'/>
          </Anchor>
        </Affix> */}
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

export default TableDemo