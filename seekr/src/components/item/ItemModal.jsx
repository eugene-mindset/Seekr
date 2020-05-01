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
            <Modal.Header style={{backgroundColor: props.itemData.found ? '#5cb85c' : '#ffc107'}}>
            <Modal.Title>
                <div>
                    
                    <text>{props.itemData.name}</text>
                </div>
                
                <div><Tags tags={ItemTags.getStrings(props.itemData.tags).split(',')} ></Tags></div>
            </Modal.Title>
            </Modal.Header>
            
            <Modal.Body>
                <h5>{props.itemData.desc}</h5>
                <div style={{marginTop: '20px'}}>{props.itemData.images.length !== 0 ? <Card.Img variant="bottom" src={ `/api/fetch_image/${props.itemData.images[0].imageData}` } /> : <span></span>}</div>
                <div style={{marginBottom: '250px', marginLeft: '430px', marginTop: '20px'}}>
                    <b>Location of item</b>
                    <GoogleMap style={{width: '0%'}} clickable={false} loc={props.itemData.location}/>
                </div>
            </Modal.Body>
            <Modal.Dialog>
                <b className="text-muted">{"Contact: " + props.itemData.username + " " + props.itemData.email}</b>
            </Modal.Dialog>
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