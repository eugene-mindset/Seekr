import React, { Component } from 'react';
import { useContext } from 'react';
import { AuthContext } from './components/helper/AuthContext';
import { Route, Redirect } from 'react-router-dom';

const ProtectedRoute = ({ component: Component, user, ...rest }) => {

//const ProtectedRoute = ({ component: Component, user, ...rest }) => {

  const { auth, setAuth, authBody, setAuthBody } = useContext(AuthContext)

  const checkAuth = () => {
    if (auth == 'null' || auth == 'undefined') {
        console.log('WHYYYYY')
        console.log(auth)
      return false
    } else {
        console.log(auth)
      return true
    }
  }
  return (
    <Route {...rest} render={
      props => {
        if (checkAuth()) {
          console.log(checkAuth())
          console.log(auth)
          return <Component {...rest} {...props} />
        } else {
          return <Redirect to='/unauthorized' />
        }
      }
    } />
  )
}

export default ProtectedRoute;