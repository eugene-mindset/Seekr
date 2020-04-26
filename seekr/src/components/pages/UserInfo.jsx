import React, { useContext } from "react";
import Profile from "../Users/Profile";
import UserSearchedItems from "../Users/UserSearchedItems";

const UserInfo = () => {
  return (
    <div>
      <Profile></Profile>
      <UserSearchedItems></UserSearchedItems>
    </div>
  );
};



export default UserInfo;
