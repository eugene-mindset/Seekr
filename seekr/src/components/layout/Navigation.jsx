import React from 'react'
import { Nav, Navbar } from 'react-bootstrap';

export default class Navigation extends React.Component {
  render() {
    return (
      <div>
        <Navbar expand="lg" bg="dark" fixed="top">
          <Navbar.Brand href="/">Seekr: Lost and Found</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ml-auto">
              <Nav.Link href="/add">Add</Nav.Link>
              <Nav.Link href="/">Search</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Navbar>
      </div>
    );
  }
}

