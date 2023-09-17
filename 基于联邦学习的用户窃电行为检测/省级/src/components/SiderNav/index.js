import React from 'react'
import CustomMenu from "../CustomMenu/index";


const menus = [
    {
        title: '属区概览',
        icon: 'table',
        key: '/home/areamanagement'
    },
    {
        title: '联邦学习启动',
        icon: 'poweroff',
        key: '/home/starttraining',
    },
    {
        title: '联邦学习可视化',
        icon: 'area-chart',
        key: '/home/flvisualization',
        subs: [
            {
              key: '/home/flvisualization/globalmodel',
              title: '全局模型',
              icon: '',
              subs: [
                {key: '/home/flvisualization/globalmodel/singletask', title: '版本', icon: ''},
                {key: '/home/flvisualization/globalmodel/comparetask', title: '版本对比', icon: ''}
              ]
            },
            {key: '/home/flvisualization/localmodel', title: '本地模型', icon: ''},
          ]
    },
    {
        title: '联邦学习历史记录',
        icon: 'profile',
        key: '/home/historyrecord',
    },
]


class SiderNav extends React.Component {
    render() {
        return (
            <div style={{height: '850px', background:'#ffffff',borderRight:'4px solid #f5f5f5'}}>
                <CustomMenu menus={menus}/>
            </div>
        )
    }
}

export default SiderNav