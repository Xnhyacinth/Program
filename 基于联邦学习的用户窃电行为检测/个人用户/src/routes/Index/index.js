import React from 'react'
import { Layout } from 'antd'
import ContentMain from '../../components/ContentMain'
import HeaderBar from '../../components/HeaderBar'

const { Sider, Header, Content, Footer } = Layout

class Index extends React.Component {
    state = { collapsed: false }
    toggle = () => {
        // console.log(this)  状态提升后，到底是谁调用的它
        this.setState({ collapsed: !this.state.collapsed })
    }

    render() {
        // 设置Sider的minHeight可以使左右自适应对齐
        return (
            <div id='page'>
                <Layout>
                    <Header style={{ background: '#55B4AE', padding: '0 16px', height: 40 }}>
                        <HeaderBar collapsed={this.state.collapsed} onToggle={this.toggle} />
                    </Header>
                    <Layout style={{height:850}}>
                        <Content style={{background:'white'}}>
                            <ContentMain />
                        </Content>
                    </Layout>
                    <Footer style={{ textAlign: 'center' }}>《联网恢恢：基于联邦学习和联盟链的窃电行为检测系统》
                            ©2022 Created by 电网打工仔</Footer>
                </Layout>
            </div>
        );
    }
}

export default Index