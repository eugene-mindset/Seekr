import React, { useContext } from 'react'
import { AuthContext } from '../helper/AuthContext';
import { Redirect } from 'react-router';

const Logout = () => {
  const { auth, setAuth, authBody, setAuthBody } = useContext(AuthContext)

	const onClick = () => {
		console.log("logging out!");
		
		// log out
		setAuth(null);
		setAuthBody(null);
	}
	
	if (auth != 'null' && auth != 'undefined') {
		return (
			<div style={{marginTop: "100px"}}>			
				<button onClick={onClick} >
					Click me to log out
				</button>
			</div>
		);
	} else {
		// temporarily just redirect back to the search page
		return ( 
			<Redirect to="/" />
		);
	}
	
};

export default Logout;