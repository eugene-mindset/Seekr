import React, { useContext } from "react";
import { Nav, Navbar } from "react-bootstrap";
import { AuthContext } from "../helper/AuthContext";

const Navigation = () => {
  const { userID } = useContext(AuthContext);
  return (
    <div>
      <Navbar expand="lg" bg="dark" fixed="top">
        <Navbar.Brand href="/">Seekr: Lost and Found</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="ml-auto">
            <Nav.Link href="/add">Add</Nav.Link>
            <Nav.Link href="/">Search</Nav.Link>
            <Nav.Link href="/about">About</Nav.Link>
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
    </div>
  );
};

export default Navigation;
