import React, { useContext, useState } from "react";
import { Nav, Navbar } from "react-bootstrap";
import { AuthContext } from "../helper/AuthContext";
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Facebook from "../Users/Facebook";



const Navigation = () => {
  const { userID, modal, setModal } = useContext(AuthContext);

  return (
    //<div>
    <React.Fragment>
      <Navbar expand="lg" fixed="top">
        <Navbar.Brand href="/">Seekr: <text style={{color:'#ffc107'}}>Lost</text> and <text style={{color:'#5cb85c'}}>Found</text></Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ml-auto">
            <Nav.Link href="/add">Add</Nav.Link>
            <Nav.Link href="/">Search</Nav.Link>
            {userID != "null" && userID != "undefined" ? (
              <Nav.Link href="/userinfo">User Info</Nav.Link>
            ) : null}
            {userID != "null" && userID != "undefined" ? (
              <Nav.Link href="/logout">Log Out</Nav.Link>
            ) : (
              <Nav.Link href="/login">Login</Nav.Link>
            )}
          </Nav>
          
        </Navbar.Collapse>
      </Navbar>
      
    </React.Fragment>


    //</div>  {model_on == true ? <LoginModal showModal={model_on} handleClose={closeModal}/> : null}
  );
};

export default Navigation;
