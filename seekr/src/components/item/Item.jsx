import React, { Component } from 'react'
import PropTypes from 'prop-types';
import Card from 'react-bootstrap/Card'
import Button from 'react-bootstrap/Button'


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
    const { id, name, found, desc, location, imageName, timestamp } = this.props.item;
    var url = "https://www.google.com/maps/place/" + location[0].toString(10) + "+" + location[1].toString(10)
    return (
      <Card style={{ textAlign: 'left', width: "16rem", margin: '1em'}}>
        <Card.Title style={{ margin: '1em 0.8em 0.5em'}}>{ name }</Card.Title>
        <Card.Text style={{ margin: '1em 1em 0.5em'}}>{ desc }</Card.Text>
        <Button variant="success" href={ url } target='_blank' style={{ margin: '1em 0.5em 1em 1em'}}>Location</Button>{' '}
        <Button variant="danger" onClick={this.props.deleteItem.bind(this, id)}>Delete</Button>
        { imageName ? this.getImage(imageName) : <span></span>}
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
