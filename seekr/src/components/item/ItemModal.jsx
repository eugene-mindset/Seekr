import React from 'react';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import PropTypes from 'prop-types';
import GoogleMap from "../pages/GoogleMap";
import Tags from './Tags';
import ItemTags from '../helper/ItemTags';
import Image from 'react-bootstrap/Image';
import Carousel from 'react-bootstrap/Carousel';

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
                <div style={{marginTop: '20px'}}> {displayImage(props.itemData.images)}</div>
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

function displayImage(imgArray) {
    if (imgArray.length === 0) {
        return (<span></span>);
    }
    else if (imgArray.length === 1) {
        return (<Image src={ `/api/fetch_image/${imgArray[0].imageData}` } fluid />);
    } else {
        return (
            <Carousel>
                {imgArray.map((img => (
                    <Carousel.Item>
                        <Image src={ `/api/fetch_image/${img.imageData}` } fluid />
                    </Carousel.Item>
                )))}
            </Carousel>
        )
    }
}

ItemModal.propTypes = {
  showModal: PropTypes.bool.isRequired,
  handleClose: PropTypes.func.isRequired,
  itemData: PropTypes.object.isRequired
}

export default ItemModal;