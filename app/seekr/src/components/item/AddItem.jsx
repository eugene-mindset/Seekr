import React, { Component } from 'react'
import PropTypes from 'prop-types';
import { Map, InfoWindow, Marker, GoogleApiWrapper} from 'google-maps-react';
import GoogleMap from '../pages/GoogleMap';

export class AddItem extends Component {
    state = {
        name: '',
        found: false,
        desc: '',
        location: ''
        /* markers: [
            {
              title: "The marker`s title will appear as a tooltip.",
              name: "SOMA",
              position: { lat: 37.778519, lng: -122.40564 }
            }
          ] */
    }

    onClick = (e) => {
        this.setState({found: true});
    }

    onSubmit = (e) => {
        e.preventDefault();
        this.props.addItem(this.state.name, this.state.found, this.state.desc, this.state.location);
        this.setState({ name: '', found: false, desc: '', location: ''});
    }

    onChange = (e) => this.setState({ [e.target.name]: e.target.value });
    
    updateState() {
        this.setState({ location: '' });
    }

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
                        type="text" 
                        name="location" 
                        style={{ flex: '10', padding: '5px' }}
                        placeholder="Click on map to add location..."
                        value={this.state.location}
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
                <GoogleMap 
                    updateParent={ this.updateState.bind(this) } 
                />
                {/* <div>
                    <h1 className="text-center">My Maps</h1>
                    <Map
                    google={this.props.google}
                    style={{ width: "80%", margin: "auto" }}
                    className={"map"}
                    zoom={14}
                    onClick={this.onClick}
                    >
                    {this.state.markers.map((marker, index) => (
                        <Marker
                        key={index}
                        title={marker.title}
                        name={marker.name}
                        position={marker.position}
                        />
                    ))}
                    </Map>
                </div> */}
            </div>
        )
    }
}

/* GoogleApiWrapper({
    apiKey: 'AIzaSyDlUTl5jQFNPLW_z1wA_C0IXYHfwUvt8V8'
  })(GoogleMap); */

AddItem.propTypes = {
    addItem: PropTypes.func.isRequired
}

export default AddItem;/* {AddItem, GoogleApiWrapper}; */
