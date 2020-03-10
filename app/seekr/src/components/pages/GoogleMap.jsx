import React, { Component } from 'react';
import { Map, InfoWindow, Marker, GoogleApiWrapper} from 'google-maps-react';

const mapStyles = {
  width: '75%',
  height: '75%'
};

class MainMap extends Component {
  constructor(props) {
    super(props);
    this.state = {
      markers: [
        {
          title: "The marker`s title will appear as a tooltip.",
          name: "SOMA",
          position: { lat: 37.778519, lng: -122.40564 }
        }
      ]
    };
    this.onClick = this.onClick.bind(this);
  }

  onClick(t, map, coord) {
    const { latLng } = coord;
    const lat = latLng.lat();
    const lng = latLng.lng();

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
      </div>
    );
  }
}

/* export class MapContainer extends Component {
  state = {
    showingInfoWindow: false,
    activeMarker: {},
    selectedPlace: {},
  };

  onMarkerClick = (props, marker, e) =>
    this.setState({
      selectedPlace: props,
      activeMarker: marker,
      showingInfoWindow: true
    });

  render() {
    return (
      <Map google={this.props.google}
      zoom={14}
      style={mapStyles}
      initialCenter={{
       lat: 39.33020225,
       lng: -76.62183913176027
      }}>
        
        <Marker onClick={this.onMarkerClick}
                name={'Current location'} />

        <InfoWindow
          marker={this.state.activeMarker}
          visible={this.state.showingInfoWindow}>
            <div>
              <h1>{this.state.selectedPlace.name}</h1>
            </div>
        </InfoWindow>
        
      </Map>
    );
  }
} */



export default GoogleApiWrapper({
  apiKey: 'AIzaSyDlUTl5jQFNPLW_z1wA_C0IXYHfwUvt8V8'
})(MainMap);