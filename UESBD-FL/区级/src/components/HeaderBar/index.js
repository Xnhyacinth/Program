import React from 'react'
import { Icon, Badge, Dropdown, Menu, Modal } from 'antd'
import screenfull from 'screenfull'
import { inject, observer } from 'mobx-react'
import { Link, withRouter } from 'react-router-dom'

//withRouter一定要写在前面，不然路由变化不会反映到props中去
@withRouter @inject('appStore') @observer
class HeaderBar extends React.Component {
  state = {
    icon: 'arrows-alt',
    count: 100,
    visible: false,
    avatar: require('../../assets/img/avatar.png')
  }

  componentDidMount() {
    screenfull.onchange(() => {
      this.setState({
        icon: screenfull.isFullscreen ? 'shrink' : 'arrows-alt'
      })
    })
  }
  componentWillUnmount() { screenfull.off('change') }
  toggle = () => { this.props.onToggle() }
  screenfullToggle = () => {
    if (screenfull.enabled) screenfull.toggle()
  }
  logout = () => {
    this.props.appStore.toggleLogin(false)
    this.props.history.push(this.props.location.pathname)
  }
  render() {
    const { icon, visible, avatar } = this.state
    const { appStore, collapsed, location } = this.props

    const menu = (
      <Menu className='menu'>
        <Menu.Item><span onClick={this.logout}>退出登录</span></Menu.Item>
      </Menu>
    )

    return (
      <div id='headerbar' style={{ height: 40 }}>
        <div style={{ lineHeight: '40px', float: 'right' }}>
          <ul className='header-ul'>
            <li><Icon type={icon} onClick={this.screenfullToggle} /></li>
            <li>
              <Dropdown overlay={menu}>
                <img onClick={() => this.setState({ visible: true })} src={avatar} alt="" />
              </Dropdown>
            </li>
          </ul>
        </div>
      </div>
    )
  }
}

export default HeaderBar