import React, { Component } from 'react'
import PropTypes from 'prop-types';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'
import Tags from './Tags'
import ItemTags from '../helper/ItemTags'

export class Item extends Component {
  getStyle = () => {
    return{
      background: '#f4f4f4',
      padding: '10px',
      borderBottom: '1px #ccc dotted',
    }
  }

  getImage = imageName => <Card.Img variant="bottom" src={`/fetch_image/${ imageName }`} />;

  getTime = timestamp => {
    var date = new Date(timestamp * 1000);
    return date.toLocaleString();
  }


  
  render() {
    const { id, name, found, desc, location, imageName, timestamp, tags, user} = this.props.item;
    var lat = location.coordinates[0]
    var lng = location.coordinates[1]
    var url = "https://www.google.com/maps/place/" + lat.toString(10) + "+" + lng.toString(10)
    return (
      <Card style={{ textAlign: 'left', width: "16rem", margin: '1em'}}>
        <Card.Title style={{ margin: '1em 0.8em 0.5em'}}>{ name }</Card.Title>
        <Tags tags={ItemTags.getStrings(tags).split(',')} ></Tags> 
        <Card.Text style={{ margin: '1em 1em 0.5em'}}>{ desc }</Card.Text>
        <Button variant="success" href={ url } target='_blank' style={{ margin: '1em 0.5em 1em 1em'}}>Location</Button>{' '}
        <Button variant="danger" onClick={this.props.deleteItem.bind(this, id)}>Delete</Button>
        { imageName ? this.getImage(imageName) : <span></span>}
        <Card.Subtitle>
          <small className="text-muted">{"Contact: " + user.name + " " + user.email + " " + user.phone}</small>
        </Card.Subtitle>
        <Card.Footer>
          <small className="text-muted">{ found ? "Found item, " : "Lost item, " }</small>
          <small className="text-muted">{ this.getTime(timestamp) }</small>
        </Card.Footer>
      </Card>
    )
  }
}

Item.propTypes = {
  item: PropTypes.object.isRequired,
  deleteItem: PropTypes.func.isRequired
}

export default Item
