import React, { useState, useEffect } from 'react'

export const AuthContext = React.createContext();

// this component will store the authentication status as well as the 
// authenticated information that we need.
export const AuthContextProvider = ({children}) => {
	// check cookie for auth
	// previous status of authentication
	const prevAuth = document.cookie.match(new RegExp('(^| )auth=([^;]+)')) || false;
	
	// previous authentication information
	const prevAuthBody = document.cookie.match(new RegExp('(^| )authBody=([^;]+)')) || false;
	
	const [auth, setAuth] = useState(prevAuth);
	const [authBody, setAuthBody] = useState(prevAuthBody);

	// whenever auth or authBody is changed, execute useEffect
	useEffect(
		// this anonymous function will automatically update the cookies
		() => {
			document.cookie = "auth=" + auth + "; authBody=" + authBody + ";path=/";
		},
		[auth, authBody]
	)
	
	const defaultContext = {
		auth,
		setAuth,
		authBody,
		setAuthBody
	}

	return (
		<AuthContext.Provider value={defaultContext}>
			{children}
		</AuthContext.Provider>
	);
};
