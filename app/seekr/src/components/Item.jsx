import React, { Component } from 'react'
import PropTypes from 'prop-types';

export class Item extends Component {
    getStyle = () => {
        return{
            background: '#f4f4f4',
            padding: '10px',
            borderBottom: '1px #ccc dotted',
            textDecoration: this.props.item.found ?
            'line-through' : 'none'
        }
    }
    
    render() {
        const { id, name } = this.props.item;
        return (
            <div style={this.getStyle()}>
                <p>
                    <input type="checkbox" onChange={this.props.markFound.bind(this, id)}/>{' '}
                    { name }
                    <button onClick={this.props.deleteItem.bind(this, id)} style={btnStyle}>x</button>
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
    item: PropTypes.object.isRequired
}

export default Item
