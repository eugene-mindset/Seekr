import React, { Component } from 'react'
import PropTypes from 'prop-types';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import Tags from './Tags'
import ItemTags from '../helper/ItemTags'
import ItemModal from "../item/ItemModal"
import "../../../public/css/Item.css";


export class Item extends Component {

  state = {
    isShowing: false,
    isAdmin: false
  };

  getImage = images => {
    // Only returns the first image for the card
    return(<Card.Img variant="bottom" src={ `/api/fetch_image/${images[0].imageData}` } />)
  };


  getTime = timestamp => {
    var date = new Date(timestamp * 1000);
    return date.toLocaleString();
  }

  modalHandler = (show) => {
    this.setState({
        isShowing: show
    });
  }

  render() {
    const { id, name, found, desc, location, images, timestamp, tags, username, email} = this.props.item;
    var lat = location.coordinates[0]
    var lng = location.coordinates[1]

    var url = "https://www.google.com/maps/place/" + lat.toString(10) + "+" + lng.toString(10)
    return (
      <div style={{}}>
        <Card id='my-card' onClick={() => this.modalHandler(true)} border={found ? 'success' : 'warning'} style={{ textAlign: 'left', width: "16rem", margin: '1em', borderWidth: '0.25em'}}>
          <Card.Title style={{ margin: '1em 0.8em 0.5em'}}>{ name }</Card.Title>
          <Tags tags={ItemTags.getStrings(tags).split(',')} ></Tags> 
          {((email === this.props.cur_email) || this.props.isAdmin == 'true') ?  <Button style={{ margin: '1em 0.5em 1em 1em'}} variant="danger" onClick={this.props.deleteItem.bind(this, id)}>Delete</Button> : null}
          { images.length !== 0 ? this.getImage(images) : <span></span>}
          <Card.Footer>
            <small className="text-muted">{ found ? "Found item, " : "Lost item, " }</small>
            <small className="text-muted">{ this.getTime(timestamp) }</small>
          </Card.Footer>
        </Card>
        <ItemModal showModal={this.state.isShowing} handleClose={this.modalHandler} itemData={this.props.item}/>
      </div>
    )
  }
}

// 

Item.propTypes = {
  item: PropTypes.object.isRequired,
  // deleteItem: PropTypes.func.isRequired
}

export default Item
