import React, { useContext } from "react";
import { AuthContext } from "../helper/AuthContext";

const UserInfo = () => {
  const { auth, authBody } = useContext(AuthContext);

  return (
		<div style={{ marginTop: "100px" }}>
			Hi {authBody}, you are {auth}
		</div>
	);
};


export default UserInfo;
