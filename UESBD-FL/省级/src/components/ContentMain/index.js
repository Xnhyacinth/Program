import React from 'react'
// import { flushSync } from 'react-dom'
import { withRouter, Switch, Redirect } from 'react-router-dom'
import LoadableComponent from '../../utils/LoadableComponent'
import PrivateRoute from '../PrivateRoute'

const demo = LoadableComponent(() => import('../../routes/General/1'))
const Home = LoadableComponent(() => import('../../routes/Home/index'))  //参数一定要是函数，否则不会懒加载，只会代码拆分

//功能1 属区管理
const AreaManagement = LoadableComponent(() => import('../../routes/AreaManagement/index'))
//功能2 联邦学习启动
const StartTraining = LoadableComponent(() => import('../../routes/StartTraining/index'))
//功能3 联邦学习可视化
//功能3-1 联邦学习全局模型可视化
const GlobalModelVisualization = LoadableComponent(() => import('../../routes/FLVisualization/GlobalModelVisualization/index'))
//功能3-2 联邦学习全局模型对比
const GlobalModelComparison = LoadableComponent(() => import('../../routes/FLVisualization/GlobalModelComparison/index'))
//功能3-3 联邦学习本地模型
const LocalModelVisualization = LoadableComponent(() => import('../../routes/FLVisualization/LocalModelVisualization/index'))
//功能4 联邦学习历史记录
const HistoryRecord = LoadableComponent(() => import('../../routes/HistoryRecord/index'))
//历史记录详情
const HistoryDetail = LoadableComponent(() => import('../../routes/HistoryDetail/index'))
//功能5 台区异常处理

//基本组件Demo
const History = LoadableComponent(() => import('../../routes/General/History/index'))
const IconDemo = LoadableComponent(() => import('../../routes/General/IconDemo/index'))

//导航组件Demo
const DropdownDemo = LoadableComponent(() => import('../../routes/Navigation/DropdownDemo/index'))
const MenuDemo = LoadableComponent(() => import('../../routes/Navigation/MenuDemo/index'))
const StepsDemo = LoadableComponent(() => import('../../routes/Navigation/StepsDemo/index'))

//输入组件Demo
const FormDemo1 = LoadableComponent(() => import('../../routes/Entry/FormDemo/FormDemo1'))
const FormDemo2 = LoadableComponent(() => import('../../routes/Entry/FormDemo/FormDemo2'))
const UploadDemo = LoadableComponent(() => import('../../routes/Entry/UploadDemo/index'))

//显示组件Demo
const CarouselDemo = LoadableComponent(() => import('../../routes/Display/CarouselDemo/index'))
const CollapseDemo = LoadableComponent(() => import('../../routes/Display/CollapseDemo/index'))
const ListDemo = LoadableComponent(() => import('../../routes/Display/ListDemo/index'))
const TableDemo = LoadableComponent(() => import('../../routes/Display/TableDemo/index'))
const TabsDemo = LoadableComponent(() => import('../../routes/Display/TabsDemo/index'))

//反馈组件Demo
const abnormal = LoadableComponent(() => import('../../routes/Feedback/abnormal/index'))
const SpinDemo = LoadableComponent(() => import('../../routes/Feedback/SpinDemo/index'))
const ModalDemo = LoadableComponent(() => import('../../routes/Feedback/ModalDemo/index'))
const NotificationDemo = LoadableComponent(() => import('../../routes/Feedback/NotificationDemo/index'))

//其它
const Start = LoadableComponent(() => import('../../routes/Other/fl/index'))
const AnimationDemo = LoadableComponent(() => import('../../routes/Other/AnimationDemo/index'))
const GalleryDemo = LoadableComponent(() => import('../../routes/Other/GalleryDemo/index'))
const DraftDemo = LoadableComponent(() => import('../../routes/Other/DraftDemo/index'))
const ChartDemo = LoadableComponent(() => import('../../routes/Other/ChartDemo/index'))
const LoadingDemo = LoadableComponent(() => import('../../routes/Other/LoadingDemo/index'))
const ErrorPage = LoadableComponent(() => import('../../routes/Other/ErrorPage/index'))
const SpringText = LoadableComponent(() => import('../../routes/Other/SpringText/index'))

@withRouter
class ContentMain extends React.Component {
    render() {
        return (
            <div style={{ padding: 16, position: 'relative' }}>
                <Switch>
                    <PrivateRoute exact path='/home/areamanagement' component={AreaManagement}></PrivateRoute>
                    <PrivateRoute exact path='/home/starttraining' component={StartTraining}></PrivateRoute>
                    <PrivateRoute exact path='/home/flvisualization/globalmodel/singletask' component={GlobalModelVisualization}></PrivateRoute>
                    <PrivateRoute exact path='/home/flvisualization/globalmodel/comparetask' component={GlobalModelComparison}></PrivateRoute>
                    <PrivateRoute exact path='/home/flvisualization/localmodel' component={LocalModelVisualization}></PrivateRoute>
                    <PrivateRoute exact path='/home/historyrecord' component={HistoryRecord}></PrivateRoute>
                    <PrivateRoute exact path='/home/historyrecord/:version_id' component={HistoryDetail} ></PrivateRoute>


                    <PrivateRoute exact path='/home' component={Home} />
                    <PrivateRoute exact path='/home/1' component={demo} />


                    <PrivateRoute exact path='/home/history' component={History} />
                    <PrivateRoute exact path='/home/general/icon' component={IconDemo} />

                    <PrivateRoute exact path='/home/navigation/dropdown' component={DropdownDemo} />
                    <PrivateRoute exact path='/home/navigation/menu' component={MenuDemo} />
                    <PrivateRoute exact path='/home/navigation/steps' component={StepsDemo} />

                    <PrivateRoute exact path='/home/entry/form/basic-form' component={FormDemo1} />
                    <PrivateRoute exact path='/home/entry/form/step-form' component={FormDemo2} />
                    <PrivateRoute exact path='/home/entry/upload' component={UploadDemo} />

                    <PrivateRoute exact path='/home/display' component={CarouselDemo} />
                    <PrivateRoute exact path='/home/display/carousel' component={CarouselDemo} />
                    <PrivateRoute exact path='/home/display/collapse' component={CollapseDemo} />
                    <PrivateRoute exact path='/home/display/list' component={ListDemo} />
                    <PrivateRoute exact path='/home/display/table' component={TableDemo} />
                    <PrivateRoute exact path='/home/display/tabs' component={TabsDemo} />

                    <PrivateRoute exact path='/home/feedback' component={abnormal} />
                    <PrivateRoute exact path='/home/feedback/modal' component={ModalDemo} />
                    <PrivateRoute exact path='/home/feedback/notification' component={NotificationDemo} />
                    <PrivateRoute exact path='/home/feedback/spin' component={SpinDemo} />

                    <PrivateRoute exact path='/home/start' component={Start} />
                    <PrivateRoute exact path='/home/other/animation' component={AnimationDemo} />
                    <PrivateRoute exact path='/home/other/gallery' component={GalleryDemo} />
                    <PrivateRoute exact path='/home/other/draft' component={DraftDemo} />
                    <PrivateRoute exact path='/home/other/chart' component={ChartDemo} />
                    <PrivateRoute exact path='/home/other/loading' component={LoadingDemo} />
                    <PrivateRoute exact path='/home/other/404' component={ErrorPage} />
                    <PrivateRoute exact path='/home/other/springText' component={SpringText} />

                    <Redirect exact from='/' to='/home' />
                </Switch>
            </div>
        )
    }
}

export default ContentMain