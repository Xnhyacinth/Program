import React from 'react'
import { Card, Popconfirm, Button, Icon, Table, Divider, BackTop, Affix, Anchor, Form, InputNumber, Input,Badge } from 'antd'
import axios from 'axios'
import CustomBreadcrumb from '../../../components/CustomBreadcrumb/index'
import TypingCard from '../../../components/TypingCard'


const data = [];
for (let i = 0; i < 100; i++) {
  data.push({
    key: i.toString(),
    name: `用户 ${i}`,
    age: 362480422,
    usernum: `台区 ${i}`,
    score: '是',
    time: `2022年5月16日 11：0${i}`,
  });
}
const FormItem = Form.Item;
const EditableContext = React.createContext();
const EditableRow = ({ form, index, ...props }) => (
  <EditableContext.Provider value={form}>
    <tr {...props} />
  </EditableContext.Provider>
);
const EditableFormRow = Form.create()(EditableRow);

class EditableCell extends React.Component {
  getInput = () => {
    if (this.props.inputType === 'number') {
      return <InputNumber />;
    }
    return <Input />;
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
          const { getFieldDecorator } = form;
          return (
            <td {...restProps}>
              {editing ? (
                <FormItem style={{ margin: 0 }}>
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
    data7: [{
      key: '0',
      name: 'Edward King 0',
      age: '32',
      address: 'London, Park Lane no. 0',
    }, {
      key: '1',
      name: 'Edward King 1',
      age: '32',
      address: 'London, Park Lane no. 1',
    }],
    count: 2,
    data,
    editingKey: '',
  }

  componentDidMount() {
    this.getRemoteData()
  }

  // columns7 = [
  //   {
  //     title: 'name',
  //     dataIndex: 'name',
  //     width: '30%',
  //   },
  //   {
  //     title: 'age',
  //     dataIndex: 'age',
  //   },
  //   {
  //     title: 'address',
  //     dataIndex: 'address',
  //   },
  //   {
  //     title: 'operation',
  //     dataIndex: 'operation',
  //     render: (text, record) => {
  //       return (
  //         this.state.data7.length > 1 ?
  //           <Popconfirm title="Sure to delete?" onConfirm={() => this.onDelete(record.key)}>
  //             <a>Delete</a>
  //           </Popconfirm> : null
  //       )
  //     }
  //   }
  // ]
  //
  //   // {
  //   //   title: '操作',
  //   //   dataIndex: 'operation',
  //   //   render: (text, record) => {
  //   //     const editable = this.isEditing(record);
  //   //     return (
  //   //       <div>
  //   //         {editable ? (
  //   //           <span>
  //   //               <EditableContext.Consumer>
  //   //                 {form => (
  //   //                   <a

  //   //                     onClick={() => this.save(form, record.key)}
  //   //                     style={{marginRight: 8}}
  //   //                   >
  //   //                     Save
  //   //                   </a>
  //   //                 )}
  //   //               </EditableContext.Consumer>
  //   //               <Popconfirm
  //   //                 title="Sure to cancel?"
  //   //                 onConfirm={() => this.cancel(record.key)}
  //   //               >
  //   //                 <a>Cancel</a>
  //   //               </Popconfirm>
  //   //             </span>
  //   //         ) : (
  //   //           <a onClick={() => this.edit(record.key)}>关闭</a>
  //   //         )}
  //   //       </div>
  //   //     );
  //   //   },
  //   // },
  // ]
  columns = [
    {
      title: '用户',
      dataIndex: 'name',
      width: '13%',
      editable: true,
    },
    {
      title: 'ID',
      dataIndex: 'age',
      width: '15%',
      editable: true,
    },
    {
      title: '所属台区',
      dataIndex: 'usernum',
      width: '15%',
      editable: true,
    },
    {
      title: '检测结果',
      dataIndex: 'operation',
      width: '14%',
      render: () => {
        
        return (
          <div>
           <Badge status="success" text="正常" />
          </div>
        );
      },
    },
    {
      title: '检测时间',
      dataIndex: 'time',
      width: '24%',
      editable: true,
    },
    // {
    //   title: '操作',
    //   dataIndex: 'operation',
    //   render: (text, record) => {
    //     return <div>
    //       <Button  style={{ margin: 5}} type="primary"  onClick={() => this.onDelete(record.key)} >
    //         解绑
    //       </Button>
    //       <Button type="primary"  onClick={() => this.edit(record.key)} >
    //         更多
    //       </Button>
    //     </div>

    //   }
    // },
  ]

  handleChange = (pagination, filters, sorter) => {
    this.setState({
      filteredInfo: filters,
      sortedInfo: sorter,
    })
  }
  clearFilters = () => {
    this.setState({ filteredInfo: null })
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
      const pagination = { ...this.state.pagination };
      pagination.total = 200
      this.setState({
        loading: false,
        data4: res.data.results,
        pagination
      })
    })
  }

  handleTableChange = (pagination, filters, sorter) => {
    const pager = { ...this.state.pagination };
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
    const { data7, count } = this.state //本来想用data7的length来代替count，但是删除行后，length会-1
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
    this.setState({ editingKey: key });
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
        this.setState({ data: newData, editingKey: '' });
      } else {
        newData.push(data);
        this.setState({ data: newData, editingKey: '' });
      }
    });
  }

  cancel = () => {
    this.setState({ editingKey: '' });
  };

  render() {
    const rowSelection = {
      selections: true
    }
    let { sortedInfo, filteredInfo } = this.state
    sortedInfo = sortedInfo || {}
    filteredInfo = filteredInfo || {}
    const columns3 = [
      {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
        filters: [
          { text: 'Joe', value: 'Joe' },
          { text: 'Jim', value: 'Jim' },
        ],
        filteredValue: filteredInfo.name || null,
        onFilter: (value, record) => record.name.includes(value),
        sorter: (a, b) => a.name.length - b.name.length,
        sortOrder: sortedInfo.columnKey === 'name' && sortedInfo.order,
      }, {
        title: 'Age',
        dataIndex: 'age',
        key: 'age',
        sorter: (a, b) => a.age - b.age,
        sortOrder: sortedInfo.columnKey === 'age' && sortedInfo.order,
      }, {
        title: 'Address',
        dataIndex: 'address',
        key: 'address',
        filters: [
          { text: 'London', value: 'London' },
          { text: 'New York', value: 'New York' },
        ],
        filteredValue: filteredInfo.address || null,
        onFilter: (value, record) => record.address.includes(value),
        sorter: (a, b) => a.address.length - b.address.length,
        sortOrder: sortedInfo.columnKey === 'address' && sortedInfo.order,
      }]
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
        <CustomBreadcrumb arr={['信息管理', '用户信息管理']} />

        <Card bordered={false} title='台区信息' style={{ marginBottom: 10, minHeight: 440 }} id='editTable'>
          <p>
            <Button style={{ margin: 10}} onClick={this.handleAdd}>导入文件</Button>
            <Button onClick={this.handleAdd}>窃电检测</Button>
          </p>
          <Table style={styles.tableStyle} components={components} bordered dataSource={this.state.data}
            columns={columns} />
        </Card>

        <BackTop visibilityHeight={200} style={{ right: 50 }} />
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