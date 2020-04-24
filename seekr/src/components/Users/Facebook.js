import React, { Component } from 'react'
import Button from 'react-bootstrap'
//import FacebookLogin from 'react-facebook-login/dist/facebook-login-render-props'
import FacebookLogin from 'react-facebook-login'
import { Redirect } from 'react-router-dom'
import ProtectedRoute from '../../ProtectedRoute';
import { useContext } from 'react'
import { AuthContext } from '../helper/AuthContext';


const Facebook = () => {
    const { auth, setAuth, authBody, setAuthBody } = useContext(AuthContext)
    
    const sendData = () => {
        this.props.parentCallback(this.state.isLoggedIn);
    }

    const doRedirect = () => {
        return <Redirect to='/userinfo' />
    }

    const componentClicked = () => {
        console.log('CLICK!!!!')
    }

    const responseFacebook = response => {
        console.log(response);

        setAuth(response.userID);
        setAuthBody(response.email);

    }
    let faceContent;

    if(auth=='' && authBody == '') {

        return <Redirect to='/user-login'/>
    } else {

        faceContent = (
            <FacebookLogin
                appId="232984641269662"
                autoLoad={false}
                fields="name,email,picture"
                onClick={componentClicked}
                callback={responseFacebook}
                //render={renderProps => (
                //<button onClick={renderProps.onClick}>This is my custom FB button</button>
                //)}
            />
        );
        return <Redirect to="/userinfo" />

    }
    return (
        <div>
            {faceContent}
        </div>
    )
    }

    export default Facebook;
