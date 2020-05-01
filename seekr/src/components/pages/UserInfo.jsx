import React from "react";
import Profile from "../Users/Profile";
import UserSearchedItems from "../Users/UserSearchedItems";
import "../../App.css";
import { useContext } from "react";
import { AuthContext } from "../helper/AuthContext";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Alert from "react-bootstrap/Alert";

const UserInfo = () => {

  const {
    setName,
    email,
    setEmail,
    userID,
    setUserID,
    setProfilePic,
    modal,
    setModal,
    setAdmin,
  } = useContext(AuthContext);

  const closeModal = () => {
    setModal(false);
  };

  console.log("Email is: "+ typeof email);
    if (email == "null" || email == "undefined" || typeof email == undefined || typeof email == null) {
      return (
        <React.Fragment>
          <Modal size="lg" show={true} centered={true}>
          <Modal.Header>
            <Modal.Title>Login Error</Modal.Title>
          </Modal.Header>
          <Modal.Body>
          <Alert variant="danger">You must have an email linked to account for you to log in</Alert>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={closeModal} href="/logout">
              Close
            </Button>
          </Modal.Footer>
        </Modal>
        </React.Fragment>
      );
    } else {
      return (
    <div className="user-info">
      <Profile></Profile>
      <UserSearchedItems></UserSearchedItems>
    </div>
    
  );}
};



export default UserInfo;
