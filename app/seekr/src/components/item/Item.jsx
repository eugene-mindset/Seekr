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
        const { id, name, found, desc } = this.props.item;
        return (
            <div style={this.getStyle()}>
                <p>
                    { name.concat(':') } { desc }
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
