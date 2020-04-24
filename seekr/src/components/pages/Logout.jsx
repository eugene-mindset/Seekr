import React, { useContext } from 'react'
import { AuthContext } from '../helper/AuthContext';

const Logout = () => {
  const { auth, setAuth, authBody, setAuthBody } = useContext(AuthContext)

	const onClick = () => {
		console.log("logging out!");

		// do log out
		setAuth(null);
		setAuthBody(null);
	}
	
	return (
		<div style={{marginTop: "100px"}}>			
			<button onClick={onClick} >
				Log out!
			</button>
		</div>
	);
};

export default Logout;