import React, { useContext } from 'react'
import { AuthContext } from '../helper/AuthContext';
import { Redirect } from 'react-router';

const Logout = () => {
  const {
		setName,
		setEmail,
		userID,
		setUserID,
		setProfilePic,
		setAdmin
	} = useContext(AuthContext)

	const Logout = () => {
		// log out
		setName(null);
		setEmail(null);
		setUserID(null);
		setProfilePic(null);
		setAdmin(false);
		window.location.reload(false);

	}
	
	if (userID !== 'null' && userID !== 'undefined') {
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