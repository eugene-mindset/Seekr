import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import PropTypes from 'prop-types';
import  Facebook from './Facebook';
import CardColumns from "react-bootstrap/CardColumns";

const columnStyle = {
  display: "flex",
  flexWrap: "wrap",
  justifyContent: "center",
  marginTop: "70px",
  marginLeft: "10px"

};

export const LoginModal = (props) => {
  return (
    <div>
      <Modal size="xl" show={props.showModal}>
        <Modal.Header>
          <Modal.Title>Login Here..</Modal.Title>
        </Modal.Header>
        <Modal.Body> 
          <Facebook></Facebook>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={props.handleClose()}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}

LoginModal.propTypes = {
  showModal: PropTypes.bool.isRequired,
  handleClose: PropTypes.func.isRequired,
}

export default LoginModal;