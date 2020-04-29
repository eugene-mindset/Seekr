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

	const Logout = () => {
		console.log("logging out!");
		
		// log out
		setName(null);
		setEmail(null);
		setUserID(null);
		setProfilePic(null);
		window.location.reload(false);

	}
	
	if (userID != 'null' && userID != 'undefined') {
		Logout()
		return (
			<Redirect to="/" />
		);
	} else {
		return ( 
			<Redirect to="/" />
		);
	}
	
};

export default Logout;