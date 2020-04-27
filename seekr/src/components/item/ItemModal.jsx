import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import PropTypes from 'prop-types';
import Items from './Items'
import CardColumns from "react-bootstrap/CardColumns";

const columnStyle = {
  display: "flex",
  flexWrap: "wrap",
  justifyContent: "center",
  marginTop: "70px",
  marginLeft: "10px"

};

export const ItemModal = (props) => {
  return (
    <div>
      <Modal size="xl" show={props.showModal} close={() => props.handleClose()}>
        <Modal.Header>
          <Modal.Title>Item Data</Modal.Title>
        </Modal.Header>
        <Modal.Body>More details about this item...
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => props.handleClose()}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}

ItemModal.propTypes = {
  showModal: PropTypes.bool.isRequired,
  handleClose: PropTypes.func.isRequired
}

export default ItemModal;