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

export const SubmissionModal = (props) => {
  return (
    <div>
      <Modal size="xl" show={props.showModal}>
        <Modal.Header>
          <Modal.Title>Before you submit...</Modal.Title>
        </Modal.Header>
        <Modal.Body>There are item listings that are similar to what you are looking for...
          <CardColumns style={columnStyle}>
            <Items items={props.simItems} deleteItem={()=>{}}/>
          </CardColumns>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => props.handleClose(false)}>
            Close
          </Button>
          <Button variant="primary" onClick={() => props.handleClose(true)}>
            Continue Submitting
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}

SubmissionModal.propTypes = {
  showModal: PropTypes.bool.isRequired,
  handleClose: PropTypes.func.isRequired,
  simItems: PropTypes.array.isRequired
}

export default SubmissionModal;