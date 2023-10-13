import React from 'react'
import CustomMenu from "../CustomMenu/index";
import '../SiderNav/style.css'

const menus = [
  {
    title: '联邦学习可视化',
    icon: 'area-chart',
    key: '/home/flvisualization'
  },
  {
    title: '信息管理',
    icon: 'edit',
    key: '/home/management',
    subs: [
      { key: '/home/management/courtsmanagement', title: '台区信息管理', icon: '' },
      {
        key: '/home/management/usermanagement',
        title: '用户信息管理',
        icon: '',
        subs: [
          { key: '/home/management/usermanagement/userlist', title: '用户列表', icon: '' },
          { key: '/home/management/usermanagement/userblacklist', title: '用户黑名单', icon: '' }
        ]
      },
    ]
  },
  {
    title: '窃电检测',
    icon: 'bulb',
    key: '/home/theftdetection',
  },
]

class SiderNav extends React.Component {
  render() {
    return (
      <div style={{ height: '850px', background: '#ffffff', borderRight: '4px solid #f5f5f5' }}>
        <CustomMenu menus={menus} />
      </div>
    )
  }
}
const styles = {}

export default SiderNav