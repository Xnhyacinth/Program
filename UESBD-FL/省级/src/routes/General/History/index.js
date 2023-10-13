import React from 'react'
import {
    Button,
    Table,
    BackTop,
    Form,
    InputNumber,
    Input,
} from 'antd'
import axios from 'axios'
import CustomBreadcrumb from '../../../components/CustomBreadcrumb/index'


const data = [];
data.push({
    key:"1",
    version: "T001",
    date:"2022-4-12",
    precision:"94.5%",
    model_tag: "全局模型",
    description: `基于多头注意力机制的窃电行为检测模型训练 聚合算法：联邦平均（常规）`,
})
data.push({
    key:"1",
    version: "T002",
    date:"2022-5-12",
    precision:"94.8%",
    model_tag: "全局模型",
    description: `基于多头注意力机制的窃电行为检测模型训练 聚合算法：联邦平均（LA）`,
})

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
        pagination: {
            pageSize: 8
        },
        data,
        editingKey: '',
    }

    componentDidMount() {
        this.getRemoteData()
    }

    columns = [
        {
            title: '版本',
            dataIndex: 'version',
            width: '8%',
            editable: true,
        },
        {
            title: '训练日期',
            dataIndex: 'date',
            width: '13%',
            editable: true,
        },
        {
            title: '最终准确率',
            dataIndex: 'precision',
            width: '11%',
            editable: true,
        },
        {
            title: '描述',
            dataIndex: 'description',
            width: '45%',
            editable: true,
        },
        {
            title: '模型文件',
            dataIndex: 'version',
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
        {
            title: '查看详情',
            dataIndex: 'version',
            render: (text, record) => {
                return <div style={{textAlign: 'center'}}>
                    <Button type="primary" shape="round" onClick={() => {
                        this.props.history.push({
                            pathname: '/home/history/' + text.toString(),
                            state: {version_id: text}
                        })
                        // this.props.history.push('/home/history/' + text.toString())
                    }}>
                        详情
                    </Button>

                </div>

            }
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

    render() {
        const rowSelection = {
            selections: true
        }
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
        const cardContent = `<ul class="card-ul">
            <li>当有大量结构化的数据需要展现时</li>
            <li>标当需要对数据进行排序、搜索、分页、自定义操作等复杂行为时</li>
          </ul>`
        return (
            <div>
                <CustomBreadcrumb arr={['联邦学习历史记录']}/>

                {/* <Card bordered={false} title='台区信息' style={{ marginBottom: 10, minHeight: 440 }} id='editTable'> */}

                <Table style={styles.tableStyle} components={components} bordered dataSource={this.state.data}
                       columns={columns}/>
                <p>
                    共有{data.length}条记录
                </p>
                {/* </Card> */}
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