import React, { useContext } from "react";
import Profile from "../Users/Profile";
import UserSearchedItems from "../Users/UserSearchedItems";
import "../../App.css";

const UserInfo = () => {
  return (
    <div className="user-info">
      <Profile></Profile>
      <UserSearchedItems></UserSearchedItems>
    </div>
  );
};



export default UserInfo;
