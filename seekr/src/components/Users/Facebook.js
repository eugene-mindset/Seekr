import React, { Component } from 'react'
import Button from 'react-bootstrap'
import FacebookLogin from 'react-facebook-login/dist/facebook-login-render-props'
import { Redirect } from 'react-router-dom'


export default class Facebook extends Component {
    constructor(props) {
        super(props);
        state = {
            isLoggedIn: false,
            userID: '',
            name: '',
            email: '',
            picture: ''
        }
      }
    


    componentClicked = () => console.log('clicked');

    doRedirect = () => {
        return <Redirect to='/user-login' />
    }

    responseFacebook = response => {
        console.log(response);

        this.setState({
            isLoggedIn: true,
            name: response.userID,
            email: response.email,
            picture: response.picture.data.url
        });

    }
    render() {
        let faceContent;

        if(this.state.isLoggedIn) {
            return <Redirect to='/user-login' />
        } else {

            faceContent = (
                <FacebookLogin
                  appId="232984641269662"
                  autoLoad={false}
                  fields="name,email,picture"
                  onClick={this.componentClicked}
                  callback={this.responseFacebook}
                  render={renderProps => (
                  <button onClick={renderProps.onClick}>This is my custom FB button</button>
                  )}
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
