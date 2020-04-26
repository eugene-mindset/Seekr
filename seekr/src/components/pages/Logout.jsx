import React, { useContext } from 'react'
import { AuthContext } from '../helper/AuthContext';
import { Redirect } from 'react-router';

const Logout = () => {
  const {
		setName,
		setEmail,
		userID,
		setUserID,
		setProfilePic
	} = useContext(AuthContext)

	const onClick = () => {
		console.log("logging out!");
		
		// log out
		setName(null);
		setEmail(null);
		setUserID(null);
		setProfilePic(null);
		return <Redirect to="/" />
	}
	
	if (userID != 'null' && userID != 'undefined') {
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