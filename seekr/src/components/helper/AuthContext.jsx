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
	const prevName = getCookieValue("name") || null;
	
	// previous authentication information
	const prevEmail = getCookieValue("email") || null;

	const prevUserID = getCookieValue("userID") || null;

	const prevProfilePic = getCookieValue("profilePic") || null;

	
	const [name, setName] = useState(prevName);
	/**
	 * state {
	 * 	auth: prevAuth
	 * }
	 * 
	 * this.setState{ auth: hello } == setAuth(hello)
	 * 
	 */
	const [email, setEmail] = useState(prevEmail);
	const [userID, setUserID] = useState(prevUserID);
	const [profilePic, setProfilePic] = useState(prevProfilePic);

	// whenever auth or authBody is changed, execute useEffect
	useEffect(
		// this anonymous function will automatically update the cookies
		() => {
			document.cookie = "name=" + auth + "; path=/";
			document.cookie = "email=" + authBody + "; path=/";
			document.cookie = "userID=" + userID + "; path=/";
			document.cookie = "profilePic=" + profilePic +"; path=/";
		},
		[auth, authBody]
	)
	
	const defaultContext = {
		name,
		setName,
		email,
		setEmail,
		userId,
		setUserID,
		profilePic,
		setProfilePic
	}

	return (
		<AuthContext.Provider value={defaultContext}>
			{children}
		</AuthContext.Provider>
	);
};
