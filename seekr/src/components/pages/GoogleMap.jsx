import React, { Component } from 'react';
import { Map, Marker, GoogleApiWrapper} from 'google-maps-react';
import PropTypes from 'prop-types';

export class GoogleMap extends Component {
  constructor(props) {
    super(props);
    if (this.props.clickable) {
      this.state = {
        markers: [
          {name: '',
          position: { lat: 39.3299, lng: -76.6205 },
          title: ''}
        ],
        location: [ 39.3299, -76.6205 ]
      };
    } else {
      this.state = {
        markers: [
          {name: '',
          position: { lat: this.props.loc.coordinates[0], lng: this.props.loc.coordinates[1] },
          title: ''}
        ],
        location: this.props.loc.coordinates
      };
    }
    
    this.onClick = this.onClick.bind(this);
  }

  sendData = () => {
    this.props.parentCallback(this.state.location);
  }

  onClick(t, map, coord) {
    if(this.props.clickable) {
      const { latLng } = coord;
      const lat = latLng.lat();
      const lng = latLng.lng();
      this.state.markers.pop();
      this.setState({location: [ lat, lng ]});
      this.sendData();
      this.setState(previousState => {
        return {
          markers: [
            ...previousState.markers,
            {
              title: "",
              name: "",
              position: { lat, lng }
            }
          ]
        };
      });
    }
    
  }

  render() {
    return (
        <Map
          google={this.props.google}
          style={{ width: "250px", height:"250px"}}
          zoom={15}
          onClick={this.onClick}
          initialCenter={this.state.markers.length !== 0 ? this.state.markers[0].position : [ 39.3299, -76.6205 ]}
          containerStyle={{ width: '250px', height: '250px' }}
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
    );
  }
}

GoogleMap.propTypes = {
  clickable: PropTypes.bool.isRequired,
  loc: PropTypes.object
}

export default GoogleApiWrapper({
  apiKey: 'AIzaSyDlUTl5jQFNPLW_z1wA_C0IXYHfwUvt8V8'
})(GoogleMap);