import React from "react";
import FacebookLogin from "react-facebook-login";
import GoogleLogin from "react-google-login";
import { Redirect } from "react-router-dom";
import { useContext } from "react";
import { AuthContext } from "../helper/AuthContext";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import axios from "axios";


const Facebook = () => {
  const {
    setName,
    setEmail,
    userID,
    setUserID,
    setProfilePic,
    modal,
    setModal,
    isAdmin,
    setAdmin,
  } = useContext(AuthContext);

  const closeModal = () => {
    setModal(false);
  };

  const startModal = () => {
    setModal(true);
  };

  const columnStyle = {
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "center",
    marginTop: "70px",
    marginLeft: "10px",
  };

  const componentClicked = () => {
    // console.log("CLICK!!!!");
  };

  const responseGoogle = (response) => {
    setUserID(response.profileObj.googleId);
    setEmail(response.profileObj.email);
    setName(response.profileObj.name);
    setProfilePic(response.profileObj.imageUrl);

    var data = new FormData();
    data.append("username", response.profileObj.name);
    data.append("email", response.profileObj.email);
    data.append("optIn", "false");

    axios({
      method: "post",
      url: "/api/userinfo",
      data: data,
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((res) => setAdmin(res.data.isAdmin));
    
    window.location.reload(false);
  };

  const responseFacebook = (response) => {
    setUserID(response.userID);
    setEmail(response.email);
    setName(response.name);
    setProfilePic(response.picture.data.url);

    var data = new FormData();
    data.append("username", response.name);
    data.append("email", response.email);
    data.append("optIn", "false");

    axios({
      method: "post",
      url: "/api/userinfo",
      data: data,
      headers: { "Content-Type": "multipart/form-data" },
    })
    .then((res) => setAdmin(res.data.isAdmin));

    window.location.reload(false);

  };
  let faceContent;
  let googleContent;

  if (userID === "null" || userID === "undefined") {
    faceContent = (
      <FacebookLogin
        appId="2484603928503868" //prod mode app id
        // appId="232984641269662" //dev mode app id
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

    return (
      <React.Fragment>
        <Modal size="sm" show={modal} centered={true}>
          <Modal.Header>
            <Modal.Title>Sign In Authentication</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {faceContent}
            <br /> <br /> {googleContent}
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={closeModal} href="/">
              Close
            </Button>
          </Modal.Footer>
        </Modal>
      </React.Fragment>
    );
  } else {
    setModal(false);
    setTimeout(() => {console.log("waiting 0.5 seconds")}, 500);
    return <Redirect to="/userinfo" />;
  }
};

export default Facebook;
