import React from 'react'
import { notification } from 'antd'
import './style.css'
import { withRouter } from 'react-router-dom'
import { inject, observer } from 'mobx-react/index'
import { preloadingImages } from '../../utils/utils'
import 'animate.css'
import LoginForm from './LoginForm'

//const url = 'http://47.99.130.140/imgs/wallhaven-g83v2e.jpg'
const url = './background.jpg'
const imgs = [
  'http://47.99.130.140/imgs/wallhaven-p8r1e9.jpg',
  'http://47.99.130.140/imgs/wallhaven-e7zyy8.jpg',
  'http://47.99.130.140/imgs/wallhaven-6k9e7q.jpg',
  'http://47.99.130.140/imgs/photo.jpg',
]

@withRouter @inject('appStore') @observer
class Login extends React.Component {
  state = {
    url: '',  //背景图片
    loading: false,
  }

  componentDidMount() {
    const isLogin = this.props.appStore
    if (isLogin) {
      this.props.appStore.toggleLogin(false) //也可以设置退出登录
    }
    this.initPage()
    preloadingImages(imgs)  //预加载
  }

  componentWillUnmount() {
    this.particle && this.particle.destory()
    notification.destroy()
  }

  initPage() {
    this.setState({ loading: true })

    this.props.appStore.initUsers()
    this.loadImageAsync(url).then(url => {
      this.setState({
        loading: false,
        url
      })
    })
  }

  //登录的背景图太大，等载入完后再显示，实际上是图片预加载，
  loadImageAsync(url) {
    return new Promise(function (resolve, reject) {
      const image = new Image();
      image.onload = function () {
        resolve(url);
      };
      image.onerror = function () {
        console.log('图片载入错误')
      };
      image.src = url;
    });
  }

  render() {
    return (
      <div id='login-page'>
        <div id='backgroundBox' style={styles.backgroundBox} />
        <div className='container'>
          <LoginForm className='box showBox'></LoginForm>
        </div>
      </div>
    )
  }
}

const styles = {
  backgroundBox: {
    position: 'fixed',
    top: '0',
    left: '0',
    width: '100vw',
    height: '100vh',
    backgroundImage: `url(${url})`,
    backgroundSize: 'cover',
    transition: 'all .5s',
    opacity: '1'
  },
  focus: {
    width: '20px',
    opacity: 1
  },
  loadingBox: {
    position: 'fixed',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%,-50%)'
  },
  loadingTitle: {
    position: 'fixed',
    top: '50%',
    left: '50%',
    marginLeft: -45,
    marginTop: -18,
    color: '#000',
    fontWeight: 500,
    fontSize: 24
  },
}

export default Login
