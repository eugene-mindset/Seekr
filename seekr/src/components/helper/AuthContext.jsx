import React, { useState, useEffect } from 'react'

export const AuthContext = React.createContext();

function getCookieValue(a) {
	let b = document.cookie.match('(^|[^;]+)\\s*' + a + '\\s*=\\s*([^;]+)');
	return b ? b.pop() : null;
}

// this component will store the authentication status as well as the 
// authenticated information that we need.
export const AuthContextProvider = ({children}) => {
	// check cookie for auth
	// previous status of authentication
	const prevAuth = getCookieValue("auth") || null;
	
	// previous authentication information
	const prevAuthBody = getCookieValue("authBody") || null;
	
	const [auth, setAuth] = useState(prevAuth);
	/**
	 * state {
	 * 	auth: prevAuth
	 * }
	 * 
	 * this.setState{ auth: hello } == setAuth(hello)
	 * 
	 */
	const [authBody, setAuthBody] = useState(prevAuthBody);

	// whenever auth or authBody is changed, execute useEffect
	useEffect(
		// this anonymous function will automatically update the cookies
		() => {
			document.cookie = "auth=" + auth + "; path=/";
			document.cookie = "authBody=" + authBody + "; path=/";
		},
		[auth, authBody]
	)
	
	const defaultContext = {
		auth: '',
		setAuth,
		authBody: '',
		setAuthBody
	}

	return (
		<AuthContext.Provider value={defaultContext}>
			{children}
		</AuthContext.Provider>
	);
};
