import React, { Component } from 'react'
import PropTypes from 'prop-types';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import Tags from './Tags'
import ItemTags from '../helper/ItemTags'

export class Item extends Component {

  getImage = images => {
    // Only returns the first image for now
    let imageLink = 'data:' + images[0].imageType + ';base64,' + images[0].imageData;
    return(<Card.Img variant="bottom" src={ imageLink } />)
  };


  getTime = timestamp => {
    var date = new Date(timestamp * 1000);
    return date.toLocaleString();
  }

  
  render() {
    const { id, name, found, desc, location, images, timestamp, tags, user} = this.props.item;
    var lat = location.coordinates[0]
    var lng = location.coordinates[1]
    var url = "https://www.google.com/maps/place/" + lat.toString(10) + "+" + lng.toString(10)
    // dummy stuff cuz too lazy to convert to hooks
    var auth = 'null'
    return (
      <Card style={{ textAlign: 'left', width: "16rem", margin: '1em'}}>
        <Card.Title style={{ margin: '1em 0.8em 0.5em'}}>{ name }</Card.Title>
        <Tags tags={ItemTags.getStrings(tags).split(',')} ></Tags> 
        <Card.Text style={{ margin: '1em 1em 0.5em'}}>{ desc }</Card.Text>
        <Button variant="success" href={ url } target='_blank' style={{ margin: '1em 0.5em 1em 1em'}}>Location</Button>{' '}
        {auth!='null' && auth!='undefined' ?  <Button variant="danger" onClick={this.props.deleteItem.bind(this, id)}>Delete</Button> : null}
        { images.length !== 0 ? this.getImage(images) : <span></span>}
        <Card.Subtitle>
          <small className="text-muted">{"Contact: " + user.name + " " + user.email}</small>
        </Card.Subtitle>
        <Card.Footer>
          <small className="text-muted">{ found ? "Found item, " : "Lost item, " }</small>
          <small className="text-muted">{ this.getTime(timestamp) }</small>
        </Card.Footer>
      </Card>
    )
  }
}

// 

Item.propTypes = {
  item: PropTypes.object.isRequired,
  // deleteItem: PropTypes.func.isRequired
}

export default Item
