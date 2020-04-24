import React, { useContext } from 'react'
import { AuthContext } from '../helper/AuthContext';

const Login = () => {
  const { auth, setAuth, authBody, setAuthBody } = useContext(AuthContext)

	const onClick = () => {
		console.log("logging in");
		setAuth("user");
		setAuthBody("Andrew");
		console.log("auth is now: " + auth);
		console.log("authBody is now: " + authBody);
	}

	return (
		<div style={{marginTop: "100px"}}>
			{/* press button to login */}
			<button onClick={onClick}>
				Log in!
			</button>
		</div>
	);
};

export default Login;