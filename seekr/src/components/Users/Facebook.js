import React from "react";
import FacebookLogin from "react-facebook-login";
import { Redirect } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../helper/AuthContext";
import axios from "axios";

const adminEmails = ["yifanandrew@yahoo.com"];


const Facebook = () => {
  const { setName, setEmail, userID, setUserID, setProfilePic, isAdmin, setAdmin } = useContext(
    AuthContext
  );

  const sendData = () => {
    this.props.parentCallback(this.state.isLoggedIn);
  };

  const doRedirect = () => {
    return <Redirect to="/userinfo" />;
  };

  const componentClicked = () => {
    console.log("CLICK!!!!");
  };


  const responseFacebook = (response) => {
    console.log(response);

    setUserID(response.userID);
    setEmail(response.email);
    setName(response.name);
    setProfilePic(response.picture.data.url);
    setAdmin(adminEmails.includes(response.email));
    

    var data = new FormData();
    data.append("username", response.name);
    data.append("email", response.email);
    data.append("optIn", 'false');
    data.append("isAdmin", adminEmails.includes(response.email));

    axios({
        method: "post",
        url: "/api/userinfo",
        data: data,
        headers: { "Content-Type": "multipart/form-data" },
      });
    
      return <Redirect to="/" />;
  };
  let faceContent;

  if (userID === "null" || userID === "undefined") {
    faceContent = (
      <FacebookLogin
        // appId="2484603928503868" //prod mode app id
        appId="232984641269662" //dev mode app id
        autoLoad={false}
        fields="name,email,picture"
        onClick={componentClicked}
        callback={responseFacebook}
      />
    );
    return <div>{faceContent}</div>;
  }
  else {
    return (
      <Redirect to="/userinfo" />
    )
  }
};

export default Facebook;
