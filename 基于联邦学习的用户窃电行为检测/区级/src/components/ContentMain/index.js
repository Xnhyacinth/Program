import React from 'react'
import { flushSync } from 'react-dom'
import { withRouter, Switch, Redirect } from 'react-router-dom'
import LoadableComponent from '../../utils/LoadableComponent'
import PrivateRoute from '../PrivateRoute'

//首页（窃电检测）
const Home = LoadableComponent(() => import('../../routes/TheftDetection/index'))

//功能1 窃电检测
const TheftDetection = LoadableComponent(() => import('../../routes/TheftDetection/index'))

//功能2 联邦学习可视化
const FLVisualization = LoadableComponent(() => import('../../routes/FLVisualization/index'))

//功能3 管理
//功能3-1 台区管理
const CourtsManagement = LoadableComponent(() => import('../../routes/Management/CourtsManagement/index'))

//功能3-2-1 用户管理
const UserList = LoadableComponent(() => import('../../routes/Management/UserList/index'))

//功能3-2-2 用户黑名单 
const UserBlackList = LoadableComponent(() => import('../../routes/Management/UerBlackList/index'))


//基本组件Demo
//const IconDemo = LoadableComponent(() => import('../../routes/General/IconDemo/index'))

//导航组件Demo
//const DropdownDemo = LoadableComponent(() => import('../../routes/Navigation/DropdownDemo/index'))
//const MenuDemo = LoadableComponent(() => import('../../routes/Navigation/MenuDemo/index'))
//const StepsDemo = LoadableComponent(() => import('../../routes/Navigation/StepsDemo/index'))

//输入组件Demo
//const FormDemo1 = LoadableComponent(() => import('../../routes/Entry/FormDemo/FormDemo1'))
//const FormDemo2 = LoadableComponent(() => import('../../routes/Entry/FormDemo/FormDemo2'))
//const UploadDemo = LoadableComponent(() => import('../../routes/Entry/UploadDemo/index'))

//显示组件Demo
//const CarouselDemo = LoadableComponent(() => import('../../routes/Display/CarouselDemo/index'))
//const CollapseDemo = LoadableComponent(() => import('../../routes/Display/CollapseDemo/index'))
//const ListDemo = LoadableComponent(() => import('../../routes/Display/ListDemo/index'))
//const TableDemo = LoadableComponent(() => import('../../routes/Display/TableDemo/index'))
//const TabsDemo = LoadableComponent(() => import('../../routes/Display/TabsDemo/index'))

//反馈组件Demo
//const abnormal = LoadableComponent(() => import('../../routes/Feedback/abnormal/index'))
//const SpinDemo = LoadableComponent(() => import('../../routes/Feedback/SpinDemo/index'))
//const ModalDemo = LoadableComponent(() => import('../../routes/Feedback/ModalDemo/index'))
//const NotificationDemo = LoadableComponent(() => import('../../routes/Feedback/NotificationDemo/index'))

//其它
/*const fl = LoadableComponent(() => import('../../routes/Other/fl/index'))
const AnimationDemo = LoadableComponent(() => import('../../routes/Other/AnimationDemo/index'))
const GalleryDemo = LoadableComponent(() => import('../../routes/Other/GalleryDemo/index'))
const DraftDemo = LoadableComponent(() => import('../../routes/Other/DraftDemo/index'))
const ChartDemo = LoadableComponent(() => import('../../routes/Other/ChartDemo/index'))
const LoadingDemo = LoadableComponent(() => import('../../routes/Other/LoadingDemo/index'))
const ErrorPage = LoadableComponent(() => import('../../routes/Other/ErrorPage/index'))
const SpringText = LoadableComponent(() => import('../../routes/Other/SpringText/index'))

//关于
const About = LoadableComponent(() => import('../../routes/About/index'))*/

@withRouter
class ContentMain extends React.Component {
  render() {
    return (
      <div style={{ padding: 16, position: 'relative' }}>
        <Switch>
          <PrivateRoute exact path='/home' component={Home} />
          <PrivateRoute exact path='/home/theftdetection' component={TheftDetection} />
          <PrivateRoute exact path='/home/flvisualization' component={FLVisualization} />
          <PrivateRoute exact path='/home/management/courtsmanagement' component={CourtsManagement} />
          <PrivateRoute exact path='/home/management/usermanagement/userlist' component={UserList} />
          <PrivateRoute exact path='/home/management/usermanagement/userblacklist' component={UserBlackList} />

{/*
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

          <PrivateRoute exact path='/home/other' component={fl} />
          <PrivateRoute exact path='/home/other/animation' component={AnimationDemo} />
          <PrivateRoute exact path='/home/other/gallery' component={GalleryDemo} />
          <PrivateRoute exact path='/home/other/draft' component={DraftDemo} />
          <PrivateRoute exact path='/home/other/chart' component={ChartDemo} />
          <PrivateRoute exact path='/home/other/loading' component={LoadingDemo} />
          <PrivateRoute exact path='/home/other/404' component={ErrorPage} />
          <PrivateRoute exact path='/home/other/springText' component={SpringText} />

          <PrivateRoute exact path='/home/about' component={About} />*/}

          <Redirect exact from='/' to='/home' />
        </Switch>
      </div>
    )
  }
}

export default ContentMain