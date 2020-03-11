import React, { Component } from 'react';
import { Map, GoogleApiWrapper } from 'google-maps-react';

const mapStyles = {
  width: '50%',
  height: '50%'
};

export class MapContainer extends Component {
  render() {
    return (
      <Map
        google={this.props.google}
        zoom={14}
        style={mapStyles}
        initialCenter={{
         lat: 39.3299013,
         lng: -76.6227065
        }}
      />
    );
  }
}

export default GoogleApiWrapper({
  apiKey: 'AIzaSyDlUTl5jQFNPLW_z1wA_C0IXYHfwUvt8V8'
})(MapContainer);