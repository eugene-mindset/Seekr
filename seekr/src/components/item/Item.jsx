import React, { Component } from 'react'
import PropTypes from 'prop-types';

export class Item extends Component {
    getStyle = () => {
        return{
            background: '#f4f4f4',
            padding: '10px',
            borderBottom: '1px #ccc dotted',
        }
    }
    
    render() {
        const { id, name, found, desc, location } = this.props.item;
        var url = "https://www.google.com/maps/place/" + location[0].toString(10) + "+" + location[1].toString(10)
        return (
            <div style={this.getStyle()}>
                <p>
                    { name.concat(':') } { desc }
                    <br />
                    <a href={ url } target="_blank">Location</a>
                    <button onClick={this.props.deleteItem.bind(this, id)} style={btnStyle}>x</button>
                    <br />
                    { found ? "Found item" : "Lost item" }
                </p>
            </div>
        )
    }
}

const btnStyle = {
    background: '#ff0000',
    color: '#fff',
    border: 'none',
    padding: '5px 9px',
    borderRadius: '50%',
    cursor: 'pointer',
    float: 'right'
}

Item.propTypes = {
    item: PropTypes.object.isRequired,
    markFound: PropTypes.func.isRequired,
    deleteItem: PropTypes.func.isRequired
}

export default Item
