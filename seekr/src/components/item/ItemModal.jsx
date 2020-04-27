import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import PropTypes from 'prop-types';
import GoogleMap from "../pages/GoogleMap";
import Card from 'react-bootstrap/Card'
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
    <div onClick={e => e.stopPropagation()}>
      <Modal className="modal-container" size="xl" show={props.showModal}
          onHide={() => props.handleClose(false)}>
        <Modal.Header>
        <Modal.Title>{props.itemData.name} </Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <div>{props.itemData.desc}</div>
            <div style={{marginBottom: '310px', position: 'relative', zIndex: '0'}}><GoogleMap clickable={false}/></div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => props.handleClose(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}

ItemModal.propTypes = {
  showModal: PropTypes.bool.isRequired,
  handleClose: PropTypes.func.isRequired,
  itemData: PropTypes.object.isRequired
}

export default ItemModal;