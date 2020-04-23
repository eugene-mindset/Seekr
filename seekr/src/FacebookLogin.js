import React, { Component } from 'react'
import FacebookLogin from 'react-facebook-login'

export default class FacebookLogin extends Component {
    state = {
        isLoggedIn: false,
        userID: '',
        name: '',
        email: '',
        picture: ''
    }

    componentClicked = () => console.log('clicked');

    responseFacebook = response => {
        console.log(response);
    }
    render() {
        let faceContent;

        if(this.state.isLoggedIn) {
            faceContent = null;
        } else {

            faceContent = (
                <FacebookLogin
                  appId="232984641269662"
                  autoLoad={true}
                  fields="name,email,picture"
                  onClick={this.componentClicked}
                  callback={this.responseFacebook}
                />
              );
        }
        return (
            <div>
                {faceContent}
            </div>
        )
    }
}
