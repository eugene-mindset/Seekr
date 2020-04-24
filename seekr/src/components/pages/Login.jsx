import React, { useContext } from 'react'
import { AuthContext } from '../helper/AuthContext';
import { Redirect } from 'react-router';

const Login = () => {
  const { auth, setAuth, authBody, setAuthBody } = useContext(AuthContext)

	const onClick = () => {
		console.log("logging in");
		setAuth("user");
		setAuthBody("Andrew");
		console.log("auth is now: " + auth);
		console.log("authBody is now: " + authBody);
	}


	if (auth == "user") {
		// if logged in already, redirect to search page
		return ( 
			<Redirect to="/userinfo" />
		);
	} else {		
		return (
			<div style={{marginTop: "100px"}}>
				{/* press button to login */}
				<button onClick={onClick}>
					Log in!
				</button>
			</div>
		);
	}
};

export default Login;