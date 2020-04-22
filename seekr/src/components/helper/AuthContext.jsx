import React, { useState, useEffect } from 'react'

export const RootContext = React.createContext();

export default function AuthContext({children}) {
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
	
	const defailtContext = {
		auth,
		setAuth,
		authBody,
		setAuthBody
	}

	return (
		<RootContext.Provider value = {defaultContext}>
			{children}
		</RootContext.Provider>
	);
};
