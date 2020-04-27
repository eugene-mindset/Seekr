import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import PropTypes from 'prop-types';
import GoogleMap from "../pages/GoogleMap";
import Card from 'react-bootstrap/Card'
import Tags from './Tags'
import ItemTags from '../helper/ItemTags'

export const ItemModal = (props) => {
      
    return (
        <div onClick={e => e.stopPropagation()}>
        <Modal className="modal-container" size="xl" show={props.showModal}
            onHide={() => props.handleClose(false)}>
            <Modal.Header>
            <Modal.Title>
                <div>{props.itemData.name}</div>
                <div><Tags tags={ItemTags.getStrings(props.itemData.tags).split(',')} ></Tags></div>
            </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <div>{props.itemData.desc}</div>
                <div>{props.itemData.images.length !== 0 ? <Card.Img variant="bottom" src={ 'data:' + props.itemData.images[0].imageType + ';base64,' + props.itemData.images[0].imageData } /> : <span></span>}</div>
                <div style={{marginBottom: '310px', position: 'relative', zIndex: '0'}}><GoogleMap clickable={false} loc={props.itemData.location}/></div>
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