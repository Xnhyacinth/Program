import React from 'react'
import { Col, Row, Select, Table } from 'antd'
import CustomBreadcrumb from '../../../components/CustomBreadcrumb'
import './style.css'
import EChartsReact from 'echarts-for-react'
import * as echarts from 'echarts';

const { Option } = Select
const dataSource = [
  {
    key: '1',
    version: 'T001',
    round: 20,
    algorithm: '联邦平均',
    optimizer: 'RAdam',
    learningRate: 0.001,
    differentialPrivacy: '否',
    aggregate: "同步"
  },
  {
    key: '2',
    version: 'T002',
    round: 20,
    algorithm: '联邦平均(LA)',
    optimizer: 'RAdam',
    learningRate: 0.001,
    differentialPrivacy: '否',
    aggregate: "同步"
  },
  {
    key: '3',
    version: 'T003',
    round: 20,
    algorithm: '联邦平均(LS)',
    optimizer: 'RAdam',
    learningRate: 0.001,
    differentialPrivacy: '是',
    aggregate: "同步"
  },
];

const columns = [
  {
    title: '版本',
    dataIndex: 'version',
    key: 'version',
    align: 'center'
  },
  {
    title: '聚合轮数',
    dataIndex: 'round',
    key: 'round',
    align: 'center'
  },
  {
    title: '聚合方式',
    dataIndex: 'aggregate',
    key: 'aggregate',
    align: 'center'
  },
  {
    title: '聚合算法',
    dataIndex: 'algorithm',
    key: 'algorithm',
    align: 'center'
  },
  {
    title: '优化算法',
    dataIndex: 'optimizer',
    key: 'optimizer',
    align: 'center'
  },
  {
    title: '学习率',
    dataIndex: 'learningRate',
    key: 'learningRate',
    align: 'center'
  },
  {
    title: '差分隐私',
    dataIndex: 'differentialPrivacy',
    key: 'differentialPrivacy',
    align: 'center'
  },
];


class FLVisualization extends React.Component {
  //加载准确率曲线配置
  getAccuracyOption = () => {
    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          label: {
            backgroundColor: '#6a7985'
          }
        }
      },
      legend: {
        top: '10%',
        left: '25%',
        data: ['T001', 'T002', 'T003']
      },

      grid: {
        left: '0%', //组件距离容器左边的距离
        right: '10%',
        top: '20%',
        bottom: '0%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: false,
          data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        }
      ],
      yAxis: [
        {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: 'grey'
            }
          },
          scale: true //缩小区间
        }
      ],
      series: [
        {
          name: 'T003',
          type: 'line',
          //stack: 'Total',
          smooth: true,
          color: 'rgba(127, 177, 213, 1)',
          //areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: [
            0.916, 0.916, 0.917, 0.917, 0.919, 0.919, 0.92, 0.922, 0.922, 0.925, 0.927, 0.929, 0.931,
            0.932, 0.932, 0.935, 0.938, 0.938, 0.94, 0.941
          ]
        },
        {
          name: 'T002',
          type: 'line',
          color: 'rgba(116, 198, 164, 0.91)',
          smooth: true,
          //stack: 'Total',
          //areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: [
            0.916, 0.917, 0.915, 0.92, 0.919, 0.921, 0.926, 0.926, 0.931, 0.932,
            0.936, 0.938, 0.939, 0.942, 0.941, 0.944, 0.943, 0.946, 0.946, 0.948
          ]
        },
        {
          name: 'T001',
          type: 'line',
          smooth: true,
          color: 'rgba(205, 157, 67, 0.56)',
          //stack: 'Total',
          //areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: [
            0.917, 0.917, 0.919, 0.92, 0.921, 0.921, 0.923, 0.924, 0.926, 0.928,
            0.934, 0.937, 0.938, 0.939, 0.94, 0.946, 0.945, 0.943, 0.945, 0.945
          ]
        }
      ]
    }
  }
  //加载精确率曲线配置
  getPrecisionOption = () => {
    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          label: {
            backgroundColor: '#6a7985'
          }
        }
      },
      legend: {
        top: '10%',
        left: '30%',
        data: ['T001', 'T002', 'T003']
      },

      grid: {
        left: '10%', //组件距离容器左边的距离
        right: '10%',
        top: '20%',
        bottom: '35%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: false,
          data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        }
      ],
      yAxis: [
        {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: 'grey'
            }
          },
          max: 1,
          min: 0.5,
          scale: true //缩小区间
        }
      ],
      series: [
        {
          name: 'T003',
          type: 'line',
          //stack: 'Total',
          smooth: true,
          color: 'rgba(127, 177, 213, 1)',
          //areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: [
            0.75, 0.857, 0.9, 0.833, 0.786, 0.718, 0.763, 0.707, 0.686, 0.778,
            0.798, 0.77, 0.746, 0.732, 0.819, 0.698, 0.77, 0.786, 0.814, 0.762
          ]
        },
        {
          name: 'T002',
          type: 'line',
          color: 'rgba(116, 198, 164, 0.91)',
          smooth: true,
          //stack: 'Total',
          //areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: [
            0.643, 0.8, 0.571, 0.812, 0.737, 0.659, 0.783, 0.802, 0.741, 0.782,
            0.778, 0.769, 0.831, 0.797, 0.776, 0.808, 0.806, 0.856, 0.83, 0.788
          ],
          smooth: true
        },
        {
          name: 'T001',
          type: 'line',
          smooth: true,
          color: 'rgba(205, 157, 67, 0.56)',
          //stack: 'Total',
          //areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: [
            0.8, 0.8, 0.767, 0.745, 0.681, 0.655, 0.793, 0.753, 0.783, 0.809, 0.794,
            0.791, 0.829, 0.765, 0.815, 0.82, 0.832, 0.847, 0.817, 0.766
          ]
        }
      ]
    }
  }
  //召回率曲线配置
  getRecallOption = () => {
    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          label: {
            backgroundColor: '#6a7985'
          }
        }
      },
      legend: {
        top: '10%',
        left: '30%',
        data: ['T001', 'T002', 'T003']
      },

      grid: {
        left: '10%', //组件距离容器左边的距离
        right: '10%',
        top: '20%',
        bottom: '35%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: false,
          data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        }
      ],
      yAxis: [
        {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: 'grey'
            }
          },
          scale: true //缩小区间
        }
      ],
      series: [
        {
          name: 'T003',
          type: 'line',
          //stack: 'Total',
          smooth: true,
          color: 'rgba(127, 177, 213, 1)',
          //areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: [
            0.0249, 0.0166, 0.0249, 0.0277, 0.0609, 0.0776, 0.0803, 0.147, 0.163,
            0.175, 0.197, 0.241, 0.285, 0.31, 0.263, 0.41, 0.391, 0.377, 0.377,
            0.452
          ]
        },
        {
          name: 'T002',
          type: 'line',
          color: 'rgba(116, 198, 164, 0.91)',
          smooth: true,
          //stack: 'Total',
          //areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: [
            0.0249, 0.0332, 0.0111, 0.072, 0.0776, 0.15, 0.18, 0.18, 0.285, 0.288,
            0.349, 0.396, 0.355, 0.435, 0.44, 0.443, 0.438, 0.446, 0.46, 0.526
          ]
        },
        {
          name: 'T001',
          type: 'line',
          smooth: true,
          color: 'rgba(205, 157, 67, 0.56)',
          emphasis: {
            focus: 'series'
          },
          data: [
            0.0332, 0.0332, 0.0637, 0.097, 0.136, 0.152, 0.127, 0.152, 0.18, 0.211, 0.31, 0.346,
            0.349, 0.416, 0.38, 0.465, 0.438, 0.399, 0.457, 0.518
          ]
        }
      ]
    }
  }
  //加载F1曲线配置
  getF1Option = () => {
    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          label: {
            backgroundColor: '#6a7985'
          }
        }
      },
      legend: {
        top: '10%',
        left: '30%',
        data: ['T001', 'T002', 'T003']
      },

      grid: {
        left: '10%', //组件距离容器左边的距离
        right: '10%',
        top: '20%',
        bottom: '35%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: false,
          data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        }
      ],
      yAxis: [
        {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: 'grey'
            }
          },
          scale: true //缩小区间
        }
      ],
      series: [
        {
          name: 'T003',
          type: 'line',
          //stack: 'Total',
          smooth: true,
          color: 'rgba(127, 177, 213, 1)',
          //areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: [
            0.0483, 0.0326, 0.0485, 0.0536, 0.113, 0.14, 0.145, 0.243, 0.264, 0.285,
            0.316, 0.367, 0.413, 0.436, 0.398, 0.517, 0.518, 0.509, 0.515, 0.567
          ]
        },
        {
          name: 'T002',
          type: 'line',
          color: 'rgba(116, 198, 164, 0.91)',
          smooth: true,
          //stack: 'Total',
          //areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: [
            0.048, 0.0638, 0.0217, 0.132, 0.14, 0.244, 0.293, 0.294, 0.412, 0.421, 0.482, 0.523, 0.497, 0.563, 0.562, 0.572, 0.567, 0.587, 0.592, 0.631
          ]
        },
        {
          name: 'T001',
          type: 'line',
          smooth: true,
          color: 'rgba(205, 157, 67, 0.56)',
          //stack: 'Total',
          //areaStyle: {},
          emphasis: {
            focus: 'series'
          },
          data: [
            0.0638, 0.0638, 0.118, 0.172, 0.226, 0.247, 0.22, 0.253, 0.293, 0.334,
            0.446, 0.482, 0.491, 0.539, 0.518, 0.594, 0.574, 0.542, 0.586, 0.618
          ]
        }
      ]
    }
  }
  //加载AUC曲线配置项
  getAUCOption = () => {
    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          label: {
            backgroundColor: '#6a7985'
          }
        }
      },
      legend: {
        top: '10%',
        left: '25%',
        data: ['T001', 'T002', 'T003']
      },

      grid: {
        left: '0%', //组件距离容器左边的距离
        right: '10%',
        top: '20%',
        bottom: '0%',
        containLabel: true
      },
      xAxis: [
        {
          type: 'category',
          boundaryGap: false,
          data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        }
      ],
      yAxis: [
        {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: 'grey'
            }
          },
          scale: true //缩小区间
        }
      ],
      series: [
        {
          name: 'T003',
          type: 'line',
          smooth: true,
          color: 'rgba(127, 177, 213, 1)',
          emphasis: {
            focus: 'series'
          },
          data: [
            0.687, 0.736, 0.768, 0.796, 0.787, 0.807, 0.817, 0.83, 0.834, 0.851, 0.859,
            0.868, 0.875, 0.879, 0.891, 0.899, 0.907, 0.915, 0.918, 0.921
          ]
        },
        {
          name: 'T002',
          type: 'line',
          color: 'rgba(116, 198, 164, 0.91)',
          smooth: true,
          emphasis: {
            focus: 'series'
          },
          data: [
            0.687, 0.711, 0.76, 0.771, 0.802, 0.824, 0.842, 0.858, 0.868, 0.878,
            0.894, 0.892, 0.901, 0.911, 0.918, 0.922, 0.924, 0.927, 0.93, 0.931
          ]
        },
        {
          name: 'T001',
          type: 'line',
          smooth: true,
          color: 'rgba(205, 157, 67, 0.56)',
          emphasis: {
            focus: 'series'
          },
          data: [
            0.684, 0.717, 0.777, 0.797, 0.812, 0.824, 0.852, 0.856, 0.864, 0.876,
            0.89, 0.898, 0.908, 0.91, 0.915, 0.921, 0.926, 0.927, 0.928, 0.928
          ]
        }
      ]
    }
  }
  //加载整体性能对比
  getTotalOption = () => {
    return {
      color: ['rgba(205, 157, 67, 0.56)', 'rgba(116, 198, 164, 0.91)', 'rgba(127, 177, 213, 1)'],
      legend: {
        top: '0',
        left: '10%',
        data: ['T001', 'T002', 'T003'],

      },
      radar: {
        radius: 70,
        center: ['40%', '45%'],
        axisName: {
          formatter: '【{value}】',
          color: '#00A9A4'
        },
        indicator: [
          { name: '准确率', max: 1 },
          { name: 'F1', max: 0.7, min: 0.5 },
          { name: '精确率', max: 1 },
          { name: '召回率', max: 0.6, min: 0.4 },
          { name: 'AUC', max: 1 }
        ]
      },
      series: [
        {
          name: '不同版本',
          type: 'radar',
          data: [
            {
              value: [0.945, 0.618, 0.766, 0.518, 0.928],
              name: 'T001'
            },
            {
              value: [0.948, 0.631, 0.788, 0.526, 0.931],
              name: 'T002'
            },
            {
              value: [0.945, 0.598, 0.794, 0.479, 0.933],
              name: 'T003'
            }
          ]
        }
      ]
    }
  }

  render() {
    return (
      <div>

        <CustomBreadcrumb arr={['联邦学习可视化', '全局模型', '版本对比']} />

        <div style={{ height: 750, marginTop: 20 }}>
          <Row style={{ height: '100%' }} gutter={24}>
            <Col className="gutter-row" span={16} style={{ height: '100%' }}>
              <div style={{ height: '100%', 'padding-left': 20, 'padding-right': 20, 'border': '2px solid #bfbfbf', 'border-radius': '10px', 'box-shadow': '2px 2px 2px  #888888' }}>
                <Row type='flex' style={{ height: '40%', 'margin-bottom': '5px', 'border-bottom': '1px solid #bfbfbf' }}>
                  <div style={{ width: '70%' }}>
                    <Row type='flex' style={{ height: '10%', marginTop: 10 }}>
                      <div style={{ height: '60%', width: '15px', background: '#00A9A4', marginLeft: 20 }}></div>
                      <div style={{ width: '70%', marginLeft: 10 }}><text >版本简述</text></div>
                    </Row>
                    <Row type='flex' style={{ height: '90%', marginTop: 10, marginLeft:20}}>
                      <Table dataSource={dataSource} columns={columns} pagination={false}></Table>
                    </Row>
                  </div>

                  <div style={{ width: '30%' }}>
                    <Row type='flex' style={{ height: '10%', marginTop: 10 }}>
                      <div style={{ height: '60%', width: '5%', background: '#00A9A4', marginLeft: 0 }}></div>
                      <div style={{ width: '70%', marginLeft: 10 }}><text >整体性能对比</text></div>
                    </Row>
                    <Row type='flex' style={{ height: '10%' }}>
                      <text style={{ marginTop: 5, marginLeft: 10 }}>请选择轮次</text>
                      <Select defaultValue="20" style={{ width: 120, marginTop: 5, marginLeft: 10 }} size='small'>
                        <Option value="1">1</Option><Option value="2">2</Option>
                        <Option value="3">3</Option><Option value="4">4</Option>
                        <Option value="5">5</Option><Option value="6">6</Option>
                        <Option value="7">7</Option><Option value="8">8</Option>
                        <Option value="9">9</Option><Option value="10">10</Option>
                        <Option value="11">11</Option><Option value="12">12</Option>
                        <Option value="13">13</Option><Option value="14">14</Option>
                        <Option value="15">15</Option><Option value="16">16</Option>
                        <Option value="17">17</Option><Option value="18">18</Option>
                        <Option value="19">19</Option><Option value="20">20</Option>
                      </Select>
                    </Row>
                    <Row style={{ height: '75%' }}>
                      <EChartsReact option={this.getTotalOption()} style={{ marginLeft: '20px' }} />
                    </Row>
                  </div>
                </Row>

                <Row type='flex' style={{ height: '60%', 'margin-bottom': '0px' }}>
                  <div style={{ height: '100%', width: '50%', marginTop: 20 }}>
                    <Row type='flex' style={{ height: '5%', width: '100%', marginTop: 20 }}>
                      <div style={{ height: '100%', width: '3%', background: '#00A9A4', marginLeft: 20 }}></div>
                      <div style={{ width: '90%', marginLeft: 10 }}><text >准确率对比曲线</text></div>
                    </Row>
                    <Row style={{ height: '80%', width: '100%' }} >
                      <EChartsReact option={this.getAccuracyOption()} style={{ marginLeft: '50px', marginTop: 10 }} />
                    </Row>
                  </div>
                  <div style={{ height: '100%', width: '50%', marginTop: 20 }}>
                    <Row type='flex' style={{ height: '5%', width: '100%', marginTop: 20 }}>
                      <div style={{ height: '100%', width: '3%', background: '#00A9A4', marginLeft: 20 }}></div>
                      <div style={{ width: '90%', marginLeft: 10 }}><text >AUC对比曲线</text></div>
                    </Row>
                    <Row style={{ height: '80%', width: '100%' }} >
                      <EChartsReact option={this.getAUCOption()} style={{ marginLeft: '50px', marginTop: 10 }} />
                    </Row>
                  </div>
                </Row>
              </div>
            </Col>


            <Col className="gutter-row" span={8} style={{ height: '100%' }}>
              <div style={{ height: '100%' }}>
                <Row style={{ height: '33%', 'margin-bottom': '5px', 'border': '2px solid #bfbfbf', 'border-radius': '10px', 'box-shadow': '2px 2px 2px  #888888' }}>
                  <Row type='flex' style={{ height: '10%', width: '100%', 'margin-left': '10px' }}>
                    <div style={{ height: '100%', width: '3%', background: '#00A9A4', marginLeft: 10, marginTop: 5 }}></div>
                    <div style={{ width: '90%', marginTop: 5, marginLeft: 10 }}><text >精确率对比曲线</text></div>
                  </Row>
                  <Row style={{ height: '90%', width: '100%' }} >
                    <EChartsReact option={this.getPrecisionOption()} />
                  </Row>

                </Row>

                <Row type='flex' style={{ height: '33%', 'margin-bottom': '5px', 'border': '2px solid #bfbfbf', 'border-radius': '10px', 'box-shadow': '2px 2px 2px  #888888' }}>
                  <Row type='flex' style={{ height: '10%', width: '100%', 'margin-left': '10px' }}>
                    <div style={{ height: '100%', width: '3%', background: '#00A9A4', marginLeft: 10, marginTop: 5 }}></div>
                    <div style={{ width: '90%', marginTop: 5, marginLeft: 10 }}><text >召回率对比曲线</text></div>
                  </Row>
                  <Row style={{ height: '90%', width: '100%' }} >
                    <EChartsReact option={this.getRecallOption()} />
                  </Row>


                </Row>

                <Row type='flex' style={{ height: '33%', 'border': '2px solid #bfbfbf', 'border-radius': '10px', 'box-shadow': '2px 2px 2px  #888888' }}>
                  <Row type='flex' style={{ height: '10%', width: '100%', 'margin-left': '10px' }}>
                    <div style={{ height: '100%', width: '3%', background: '#00A9A4', marginLeft: 10, marginTop: 5 }}></div>
                    <div style={{ width: '90%', marginTop: 5, marginLeft: 10 }}><text >F1对比曲线</text></div>
                  </Row>
                  <Row style={{ height: '90%', width: '100%' }} >
                    <EChartsReact option={this.getF1Option()} />
                  </Row>

                </Row>
              </div>
            </Col>
          </Row>
        </div>

      </div>
    )
  }
}


export default FLVisualization