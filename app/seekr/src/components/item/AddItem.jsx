import React, { Component } from 'react'
import PropTypes from 'prop-types';

export class AddItem extends Component {
    state = {
        name: '',
        found: false,
        desc: ''
    }

    onClick = (e) => {
        this.setState({found: true});
    }

    onSubmit = (e) => {
        e.preventDefault();
        this.props.addItem(this.state.name, this.state.found, this.state.desc);
        this.setState({ name: '', found: false, desc: ''});
    }

    onChange = (e) => this.setState({ [e.target.name]: e.target.value });
    

    render() {
        return (
            // flexbox
            <form onSubmit={this.onSubmit} style={{ display: 'flex' }}>
                <input 
                    type="text" 
                    name="name" 
                    style={{ flex: '10', padding: '5px' }}
                    placeholder="Add Item Name..."
                    value={this.state.name}
                    onChange={this.onChange}
                />
                <input 
                    type="text" 
                    name="desc" 
                    style={{ flex: '10', padding: '5px' }}
                    placeholder="Add Item Description..."
                    value={this.state.desc}
                    onChange={this.onChange}
                />
                <input 
                    type="submit" 
                    value="List as Missing "
                    className="btn"
                    style={{ flex: '1' }}
                    
                    
                />
                <input 
                    type="submit" 
                    value="List as Found "
                    className="btn"
                    style={{ flex: '1' }}
                    onClick={this.onClick}
                />
            </form>
        )
    }
}

AddItem.propTypes = {
    addItem: PropTypes.func.isRequired
}

export default AddItem
