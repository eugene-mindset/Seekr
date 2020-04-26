import React from 'react'
import Button from 'react-bootstrap'
import FacebookLogin from 'react-facebook-login'
import { Redirect } from 'react-router-dom'
import { useContext } from 'react'
import { AuthContext } from '../helper/AuthContext';


const Facebook = () => {
    const {
		setName,
        setEmail,
        userID,
		setUserID,
		setProfilePic
    } = useContext(AuthContext)
    
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

        setUserID(response.userID);
        setEmail(response.email);
        setName(response.name);
        setProfilePic(response.profilePic);
        console.log(response.email);
        return <Redirect to="/userinfo" />

    }
    let faceContent;

    console.log(userID)
    if(userID == 'null' || userID == 'undefined') {

        faceContent = (
            <FacebookLogin
                appId="232984641269662"
                autoLoad={false}
                fields="name,email,picture"
                onClick={componentClicked}
                callback={responseFacebook}
            />
        );
    }
    return (
        <div>
            {faceContent}
        </div>
    )
    }

     export default Facebook;
