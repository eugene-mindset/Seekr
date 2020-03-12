import React, { Component } from 'react';
import { Map, Marker, GoogleApiWrapper} from 'google-maps-react';

export class GoogleMap extends Component {
  constructor(props) {
    super(props);
    this.state = {
      markers: [
        {name: '',
        position: { lat: 39.3299, lng: -76.6205 },
        title: ''}
      ],
      location: [ 39.3299, -76.6205 ]
    };
    this.onClick = this.onClick.bind(this);
  }

  sendData = () => {
    this.props.parentCallback(this.state.location);
  }
  
  onClick(t, map, coord) {
    const { latLng } = coord;
    const lat = latLng.lat();
    const lng = latLng.lng();
    this.state.markers.pop();
    this.props.updateParent;
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

  render() {
    
    return (
      <div>
        <h1 className="text-center">Drop a marker on location of lost item.</h1>
        <Map
          google={this.props.google}
          style={{ width: "80%", margin: "auto" }}
          className={"map"}
          zoom={14}
          onClick={this.onClick}
          initialCenter={{ lat: 39.3299, lng: -76.6205 }}
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
      </div>
    );
  }
}

export default GoogleApiWrapper({
  apiKey: 'AIzaSyDlUTl5jQFNPLW_z1wA_C0IXYHfwUvt8V8'
})(GoogleMap);