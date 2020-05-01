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

	const prevAdmin = getCookieValue("isAdmin") || null;
	const prevModal = getCookieValue("modal") || null;

	
	const [name, setName] = useState(prevName);
	const [email, setEmail] = useState(prevEmail);
	const [userID, setUserID] = useState(prevUserID);
	const [profilePic, setProfilePic] = useState(prevProfilePic);
	const [isAdmin, setAdmin] = useState(prevAdmin);
	const [modal, setModal] = useState(prevModal)

	useEffect(
		// this anonymous function will automatically update the cookies
		() => {
			document.cookie = "name=" + name + "; path=/";
			document.cookie = "email=" + email + "; path=/";
			document.cookie = "userID=" + userID + "; path=/";
			document.cookie = "profilePic=" + profilePic +"; path=/";
			document.cookie = "isAdmin=" + isAdmin +"; path=/";
			document.cookie = "modal=" + modal + "; path=/";
		},
		[name, email, userID, profilePic, isAdmin, modal]
	)
	
	const defaultContext = {
		name,
		setName,
		email,
		setEmail,
		userID,
		setUserID,
		profilePic,
		setProfilePic,
		isAdmin,
		setAdmin,
		modal,
		setModal
	}

	return (
		<AuthContext.Provider value={defaultContext}>
			{children}
		</AuthContext.Provider>
	);
};
