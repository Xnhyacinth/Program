import React from 'react'
// import { flushSync } from 'react-dom'
import { withRouter, Switch, Redirect } from 'react-router-dom'
import LoadableComponent from '../../utils/LoadableComponent'
import PrivateRoute from '../PrivateRoute'

const UserPage = LoadableComponent(()=>import('../../routes/UserPage/index'))


@withRouter
class ContentMain extends React.Component {
    render() {
        return (
            <div style={{ padding: 16, position: 'relative' }}>
                <Switch>
                    <PrivateRoute exact path='/home' component={UserPage} />

                    <Redirect exact from='/' to='/home' />
                </Switch>
            </div>
        )
    }
}

export default ContentMain