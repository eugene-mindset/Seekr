import React from "react";
import FacebookLogin from "react-facebook-login";
import GoogleLogin from "react-google-login";
import { Redirect } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../helper/AuthContext";
import axios from "axios";


const Facebook = () => {
  const { setName, setEmail, userID, setUserID, setProfilePic } = useContext(
    AuthContext
  );

  const componentClicked = () => {
    console.log("CLICK!!!!");
  };

  const responseGoogle = (response) => {
    console.log(response);
    console.log(response.profileObj.name);

    setUserID(response.profileObj.googleId);
    setEmail(response.profileObj.email);
    setName(response.profileObj.name);
    setProfilePic(response.profileObj.imageUrl);
    console.log(response.email);
    
    var data = new FormData();
    data.append("username", response.profileObj.name);
    data.append("email", response.profileObj.email);
    data.append("optIn", 'false');

    axios({
        method: "post",
        url: "/api/userinfo",
        data: data,
        headers: { "Content-Type": "multipart/form-data" },
      });
    
      return <Redirect to="/" />;
  };

  const responseFacebook = (response) => {
    console.log(response.email);

    setUserID(response.userID);
    setEmail(response.email);
    setName(response.name);
    setProfilePic(response.picture.data.url);
    console.log(response.email);
    
    var data = new FormData();
    data.append("username", response.name);
    data.append("email", response.email);
    data.append("optIn", 'false');

    axios({
        method: "post",
        url: "/api/userinfo",
        data: data,
        headers: { "Content-Type": "multipart/form-data" },
      });
    
      return <Redirect to="/" />;
  };
  let faceContent;
  let googleContent;

  if (userID === "null" || userID === "undefined") {
    faceContent = (
      <FacebookLogin
        //appId="2484603928503868" //prod mode app id
         appId="232984641269662" //dev mode app id
        autoLoad={false}
        fields="name,email,picture"
        onClick={componentClicked}
        callback={responseFacebook}
      />
    );

    googleContent = (
      <GoogleLogin
      clientId="939123834862-tfmmtaultoguklkc2f5ebtve50k26e93.apps.googleusercontent.com"
      buttonText="LOGIN WITH GOOGLE"
      onSuccess={responseGoogle}
      onFailure={responseGoogle}
      />
    );
    return <div>{faceContent}<br /> <br /> {googleContent}</div>;
  }
  else {
    return (
      <Redirect to="/userinfo" />
    )
  }
};

export default Facebook;
