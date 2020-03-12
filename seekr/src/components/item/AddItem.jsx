import React, { Component } from 'react'
import PropTypes from 'prop-types';
import GoogleMap from '../pages/GoogleMap';

export class AddItem extends Component {
    state = {
        name: '',
        found: false,
        desc: '',
        location: [ 39.3299, -76.6205 ]
    }

    callbackFunction = (childData) => {
        this.setState({location: childData})
    }

    onClick = (e) => {
        this.setState({found: true});
    }

    onSubmit = (e) => {
        e.preventDefault();
        this.props.addItem(this.state.name, this.state.found, this.state.desc, this.state.location);
        this.setState({ name: '', found: false, desc: ''});
    }

    onChange = (e) => this.setState({ [e.target.name]: e.target.value });

    render() {
        return (
            // flexbox
            <div>
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
                <GoogleMap parentCallback={this.callbackFunction}/>
            </div>
        )
    }
}

AddItem.propTypes = {
    addItem: PropTypes.func.isRequired
}

export default AddItem;