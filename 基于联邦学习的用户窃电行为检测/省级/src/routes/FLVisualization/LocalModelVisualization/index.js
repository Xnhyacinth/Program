import React from 'react'
import { Col, Row, Select } from 'antd'
import CustomBreadcrumb from '../../../components/CustomBreadcrumb'
import './style.css'
import EChartsReact from 'echarts-for-react'
import * as echarts from 'echarts';

const { Option } = Select

class FLVisualization extends React.Component {
  //加载准确率曲线配置
  getAccuracyOption = () => {
    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      grid: {
        left: '10%', //组件距离容器左边的距离
        right: '10%',
        top: '12%',
        bottom: '45%'
      },
      xAxis: {
        //name: 'Round',
        type: 'category',
        axisTick: {
          alignWithLabel: true
        },
        boundaryGap: false, //紧贴y轴
        data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
      },
      yAxis: {
        type: 'value',
        position: 'left',
        alignTicks: true,
        axisLine: {
          show: false,     //不显示Y轴线
          lineStyle: {
            color: 'grey'
          }
        },
        min: 0.9, // 设置y轴刻度的最小值
        max: 0.96,  // 设置y轴刻度的最大值
        scale: true //缩小区间
      },
      series: [
        {
          name: '准确率',
          type: 'line',
          data: [
            0.916, 0.916, 0.915, 0.918, 0.917, 0.92, 0.924, 0.925, 0.928, 0.925, 0.927, 0.932, 0.932, 0.935, 0.936, 0.938, 0.934, 0.933, 0.937, 0.941
          ],
          smooth: true,

          //线条属性
          lineStyle: {
            color: 'rgba(116, 198, 164, 0.91)'
          },
          //拐点属性
          itemStyle: {
            normal: {
              color: 'rgba(116, 198, 164, 0.91)'
            }
          },
          //折线下面区域属性
          areaStyle: {
            normal: {
              //颜色渐变函数 前四个参数分别表示四个位置依次为左、下、右、上
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(80,141,255,0.39)'
                },
                {
                  offset: 0.34,
                  color: 'rgba(56,155,255,0.25)'
                },
                {
                  offset: 1,
                  color: 'rgba(38,197,254,0.00)'
                }
              ])
            }
          }

        }
      ]
    }
  }
  //加载精确率、召回率、F1曲线配置
  getRecallOption = () => {
    return {
      tooltip: {
        trigger: 'axis',

      },
      grid: {
        left: '15%', //组件距离容器左边的距离
        right: '15%',
        top: '15%',
        bottom: '45%'
      },

      //legend就是有多个折线时上面的显示按钮！！！！！！！！
      legend: {
        data: ['精确率', 'F1', '召回率'],
        top: '10%',
        left: '30%'
      },
      xAxis: [
        {
          type: 'category',
          axisTick: {
            alignWithLabel: true
          },
          boundaryGap: false, //紧贴y轴
          // prettier-ignore
          data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        }
      ],
      yAxis: [
        {
          //右轴1 显示该y轴
          type: 'value',
          name: 'F1,召回率',
          position: 'right',
          alignTicks: true,
          max: 1,
          min: 0,
          axisLine: {
            show: true,
            lineStyle: {
              color: 'grey'
            }
          },
          scale: true, //缩小区间
          axisLabel: {
            formatter: '{value} '
          }
        },
        {
          //不显示该y轴 不可以不写
          type: 'value',
          position: 'right',
          show: false, //不可见！！！！
          alignTicks: true,
          offset: 80,
          axisLine: {
            show: true,
            lineStyle: {
              color: 'grey'
            }
          },
          scale: true, //缩小区间
          axisLabel: {
            formatter: '{value} ml'
          }
        },
        {
          //左轴2
          type: 'value',
          name: '精确率',
          position: 'left',
          alignTicks: true,
          axisLine: {
            show: true,
            lineStyle: {
              color: 'grey'
            }
          },
          scale: true//缩小区间
        }
      ],
      series: [
        {
          name: '精确率',
          color: 'rgba(127, 177, 213, 1)',
          type: 'line',
          yAxisIndex: 2,   //左轴
          data: [0.833, 1.0, 0.6, 0.644, 0.696, 0.714, 0.761, 0.862, 0.776, 0.817, 0.903, 0.841, 0.912, 0.82, 0.81, 0.801, 0.887, 0.882, 0.855, 0.837],
          smooth: true
        },
        {
          name: 'F1',
          color: 'rgba(116, 198, 164, 0.91)',
          type: 'line',
          yAxisIndex: 1,   //右轴
          data: [
            0.0272, 0.038, 0.0164, 0.143, 0.0833, 0.171, 0.25, 0.239, 0.331, 0.269, 0.265, 0.385, 0.367, 0.441, 0.457, 0.505, 0.403, 0.389, 0.455, 0.528],
          smooth: true
        },
        {
          name: '召回率',
          color: 'rgba(201, 197, 123, 1)',
          type: 'line',
          yAxisIndex: 1,
          data: [
            0.0139, 0.0194, 0.00831, 0.0803, 0.0443, 0.097, 0.15, 0.139, 0.211, 0.161, 0.155, 0.249, 0.23, 0.302, 0.319, 0.368, 0.26, 0.249, 0.31, 0.385],
          smooth: true
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
          type: 'cross'
        }
      },
      grid: {
        left: '15%', //组件距离容器左边的距离
        right: '10%',
        top: '10%',
        bottom: '45%'
      },
      xAxis: {
        //name: 'Round',
        type: 'category',
        axisTick: {
          alignWithLabel: true
        },

        boundaryGap: false, //紧贴y轴
        data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
      },
      yAxis: {
        type: 'value',
        position: 'left',
        alignTicks: true,
        axisLine: {
          show: false,     //不显示Y轴线
          lineStyle: {
            color: 'grey'
          }
        },

        scale: true //缩小区间
      },
      series: [
        {
          name: 'AUC',
          color: 'rgba(116, 198, 164, 0.91)',
          type: 'line',
          data: [
            0.712, 0.72, 0.731, 0.755, 0.777, 0.805, 0.841, 0.809, 0.848, 0.825, 0.879, 0.876, 0.886, 0.89, 0.896, 0.903, 0.903, 0.91, 0.915, 0.914
          ],
          smooth: true,
          //折线图的高亮状态

        }
      ]
    }
  }
  //加载Loss配置项
  getLossOption = () => {
    return {
      tooltip: {
        trigger: 'axis',
      },
      grid: {
        left: '15%', //组件距离容器左边的距离
        right: '10%',
        top: '15%',
        bottom: '45%'
      },
      xAxis: {
        //name: 'Round',
        type: 'category',
        axisTick: {
          alignWithLabel: true
        },

        boundaryGap: false, //紧贴y轴
        data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
      },
      yAxis: {
        type: 'value',
        position: 'left',
        alignTicks: true,
        axisLine: {
          show: false,     //不显示Y轴线
          lineStyle: {
            color: 'grey'
          }
        },
        scale: true //缩小区间
      },
      legend: {
        data: ['测试集损失', '训练集损失'],
        top: '5%',
        left: '30%'
      },
      series: [
        {
          name: '测试集损失',
          color: 'rgba(116, 198, 164, 0.91)',
          type: 'line',
          data: [
            0.28, 0.273, 0.267, 0.259, 0.272, 0.238, 0.222, 0.242, 0.214, 0.268, 0.223, 0.195, 0.207, 0.195, 0.188, 0.182, 0.206, 0.205, 0.195, 0.194
          ],
          smooth: true,
        },
        {
          name: '训练集损失',
          color: 'rgba(127, 177, 213, 1)',
          type: 'line',
          data: [
            0.34, 0.283, 0.274, 0.26, 0.254, 0.241, 0.232, 0.224, 0.218, 0.208, 0.199, 0.189, 0.186, 0.175, 0.168, 0.161, 0.152, 0.145, 0.133, 0.127
          ],
          smooth: true,
        }
      ]
    }
  }
  //加载MAP配置项
  getMAPOption = () => {
    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        top: '10%',
        left: '30%'
      },
      grid: {
        left: '0',
        right: '10%',
        bottom: '0%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        //boundaryGap: 'true',//[0, 0.01],
        data: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
      },
      yAxis: {
        type: 'value',
      },
      series: [
        {
          name: 'MAP@100',
          type: 'bar',
          color: 'rgba(116, 198, 164, 0.91)',
          barWidth: 7,
          showBackground: true,
          data: [0.696, 0.747, 0.544, 0.748, 0.653, 0.794, 0.852, 0.864, 0.901, 0.866, 0.905, 0.944, 0.962, 0.949, 0.94, 0.963, 0.97, 0.947, 0.918, 0.95]
        },
        {
          name: 'MAP@200',
          type: 'bar',
          color: 'rgba(127, 177, 213, 1)',
          barWidth: 7,
          showBackground: true,
          data: [0.692, 0.699, 0.56, 0.702, 0.622, 0.702, 0.776, 0.792, 0.837, 0.781, 0.784, 0.848, 0.877, 0.885, 0.882, 0.915, 0.885, 0.842, 0.864, 0.911]
        }
      ]
    }
  }
  //加载混淆矩阵配置项
  getMatrixOption = () => {

    // prettier-ignore
    var data = [[0, 0, 222], [0, 1, 139], [1, 0, 3849], [1, 1, 27]]
      .map(function (item) {
        return [item[1], item[0], item[2] || '-'];
      });

    return {
      tooltip: {
        position: 'top'
      },
      grid: {
        height: '70%',
        width: '50%',
        top: '15%',
        left: '10%'
      },
      xAxis: {
        type: 'category',
        data: ['正常', '窃电'],
        splitArea: {
          show: true,
        }
      },
      yAxis: {
        type: 'category',
        data: ['窃电', '正常'],
        splitArea: {
          show: true
        }
      },
      visualMap: {
        min: 0,
        max: 4000,
        calculable: true,
        precision: 0,
        itemWidth: 20,
        itemHeight: 210,
        align: 'right',//'top',
        orient: 'vertical',
        right: '25%',
        top: '13%',
        inRange: {
          color: ['#e6fffb', '#006d75',]
        }
      },
      series: [
        {
          type: 'heatmap',
          data: data,
          label: {
            show: true,
          },
          emphasis: {
            itemStyle: {
              borderWidth: 1,
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    }
  }

  render() {
    return (
      <div>

        <CustomBreadcrumb arr={['联邦学习可视化','本地模型']} />

        <div style={{ height: 750, marginTop: 20 }}>
          <Row style={{ height: '100%' }} gutter={24}>
            <Col className="gutter-row" span={16} style={{ height: '100%' }}>
              <div style={{ height: '100%', 'padding-left': 20, 'border': '2px solid #bfbfbf', 'border-radius': '10px', 'box-shadow': '2px 2px 2px  #888888' }}>
                <Row type='flex' align='middle' style={{ height: '40%', 'margin-bottom': '5px' }}>

                  <Col span={12} style={{ height: '80%', width: '50%' }}>
                    <Row type='flex' style={{ height: '20%', width: '100%' }} >
                      <text style={{ marginTop: 5, marginLeft: 10 }}>请选择版本</text>
                      <Select defaultValue="T002" style={{ width: 120, marginLeft: 15 }}>
                        <Option value="1">T001</Option><Option value="2">T002</Option>
                        <Option value="3">T003</Option>
                      </Select>
                      <text style={{ marginTop: 5, marginLeft: 10 }}>请选择台区编号</text>
                      <Select defaultValue="C001" style={{ width: 120, marginLeft: 15 }}>
                        <Option value="C001">C001</Option><Option value="C002">C002</Option><Option value="C003">C003</Option>
                      </Select>
                    </Row>
                    <Row type='flex' style={{ height: '10%', width: '100%' }}>
                      <div style={{ height: '100%', width: '3%', background: '#00A9A4', marginLeft: 10, marginTop: 5 }}></div>
                      <div style={{ width: '90%', marginTop: 5, marginLeft: 10 }}><text >训练任务描述</text></div>
                    </Row>
                    <div style={{ 'padding-left': '10px', 'padding-bottom': '30px', 'border-bottom': '1px solid  #bfbfbf' }}>
                      <Row type='flex' style={{ height: '15%', width: '100%', marginTop: 20 }} >
                        <div style={{ width: '12%', marginTop: 10, marginLeft: 10 }}><text >任务简介:</text></div>
                        <div style={{ marginTop: 10, marginLeft: 10 }}><text >基于多头自主意力机制窃电检测模型训练</text></div>
                      </Row>
                      <Row type='flex' style={{ height: '15%', width: '100%' }} >
                        <div style={{ width: '12%', marginTop: 10, marginLeft: 10 }}><text >聚合轮数:</text></div>
                        <div style={{ width: '15%', marginTop: 10, marginLeft: 10 }}><text >20</text></div>
                        <div style={{ width: '12%', marginTop: 10, marginLeft: 60 }}><text >聚合方式:</text></div>
                        <div style={{ marginTop: 10, marginLeft: 10 }}><text >同步</text></div>
                      </Row>
                      <Row type='flex' style={{ height: '15%', width: '100%' }} >
                        <div style={{ width: '12%', marginTop: 10, marginLeft: 10 }}><text >聚合算法:</text></div>
                        <div style={{ width: '20%', marginTop: 10, marginLeft: 10 }}><text >联邦平均(LA)</text></div>
                        <div style={{ width: '12%', marginTop: 10, marginLeft: '6%' }}><text >优化算法:</text></div>
                        <div style={{ marginTop: 10, marginLeft: 10 }}><text >RAdam</text></div>
                      </Row>
                      <Row type='flex' style={{ height: '15%', width: '100%' }} >
                        <div style={{ width: '12%', marginTop: 10, marginLeft: 10 }}><text >学习率:</text></div>
                        <div style={{ width: '2%', marginTop: 10, marginLeft: 10 }}><text >0.001</text></div>
                        <div style={{ width: '25%', marginTop: 10, marginLeft: '24%' }}><text >是否引入差分隐私:</text></div>
                        <div style={{ marginTop: 10, marginLeft: 10 }}><text >否</text></div>
                      </Row>
                    </div>


                  </Col>
                  <Col span={12} style={{ height: '80%', width: '50%' }}>
                    <Row type='flex' style={{ height: '10%', width: '100%' }}>
                      <div style={{ height: '100%', width: '3%', background: '#00A9A4', marginLeft: 20, marginTop: 5 }}></div>
                      <div style={{ width: '90%', marginTop: 5, marginLeft: 10 }}><text >准确率变化曲线</text></div>
                    </Row>
                    <Row style={{ height: '90%', width: '100%' }} >
                      <EChartsReact option={this.getAccuracyOption()} style={{ marginLeft: '50px' }} />
                    </Row>
                  </Col>

                </Row>
                <Row type='flex' style={{ height: '60%', 'margin-bottom': '0px' }}>
                  <div style={{ height: '100%', width: '50%' }}>
                    <Row type='flex' style={{ height: '5%', marginTop: 10 }}>
                      <div style={{ height: '100%', width: '3%', background: '#00A9A4', marginLeft: 10, marginTop: 5 }}></div>
                      <div style={{ width: '90%', marginTop: 5, marginLeft: 10 }}><text >混淆矩阵</text></div>
                    </Row>
                    <Row type='flex' style={{ height: '10%', marginTop: 20 }}>
                      <text style={{ marginTop: 15, marginLeft: 10 }}>请选择轮次</text>
                      <Select defaultValue="20" style={{ width: 120, marginTop: 10, marginLeft: 15 }}>
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
                      <EChartsReact option={this.getMatrixOption()} style={{ marginLeft: '20px', marginTop: 10 }} />
                    </Row>
                  </div>
                  <div style={{ height: '100%', width: '50%', marginTop: 30 }}>
                    <Row type='flex' style={{ height: '5%', width: '100%', marginTop: 20 }}>
                      <div style={{ height: '100%', width: '3%', background: '#00A9A4', marginLeft: 20 }}></div>
                      <div style={{ width: '90%', marginLeft: 10 }}><text >MAP@100、MAP@200变化曲线</text></div>
                    </Row>
                    <Row style={{ height: '80%', width: '100%' }} >
                      <EChartsReact option={this.getMAPOption()} style={{ marginLeft: '50px', marginTop: 10 }} />
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
                    <div style={{ width: '90%', marginTop: 5, marginLeft: 10 }}><text >精确率、召回率、F1变化曲线</text></div>
                  </Row>
                  <Row style={{ height: '90%', width: '100%' }} >
                    <EChartsReact option={this.getRecallOption()} />
                  </Row>

                </Row>

                <Row type='flex' style={{ height: '33%', 'margin-bottom': '5px', 'border': '2px solid #bfbfbf', 'border-radius': '10px', 'box-shadow': '2px 2px 2px  #888888' }}>
                  <Row type='flex' style={{ height: '10%', width: '100%', 'margin-left': '10px' }}>
                    <div style={{ height: '100%', width: '3%', background: '#00A9A4', marginLeft: 10, marginTop: 5 }}></div>
                    <div style={{ width: '90%', marginTop: 5, marginLeft: 10 }}><text >AUC变化曲线</text></div>
                  </Row>
                  <Row style={{ height: '90%', width: '100%' }} >
                    <EChartsReact option={this.getAUCOption()} />
                  </Row>


                </Row>

                <Row type='flex' style={{ height: '33%', 'border': '2px solid #bfbfbf', 'border-radius': '10px', 'box-shadow': '2px 2px 2px  #888888' }}>
                  <Row type='flex' style={{ height: '10%', width: '100%', 'margin-left': '10px' }}>
                    <div style={{ height: '100%', width: '3%', background: '#00A9A4', marginLeft: 10, marginTop: 5 }}></div>
                    <div style={{ width: '90%', marginTop: 5, marginLeft: 10 }}><text >训练集、测试集损失变化曲线</text></div>
                  </Row>
                  <Row style={{ height: '90%', width: '100%' }} >
                    <EChartsReact option={this.getLossOption()} />
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