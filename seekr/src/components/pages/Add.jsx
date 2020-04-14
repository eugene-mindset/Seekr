import React, { Component } from 'react';
import axios from 'axios';
import AddItem from '../item/AddItem';

export default class Add extends Component {

  addItem = (name, found, desc, location, tags, img, radius) => {
    var data = new FormData();
    data.append('name', name);
    data.append('desc', desc);
    data.append('found', found);
    data.append('location', location);
    data.append('radius', radius);
    data.append('tags', tags);
    data.append('image', img);
      
    axios({
      method: 'post',
      url: '/items',
      data: data,
      headers: {'Content-Type': 'multipart/form-data' }
      });
  }

  render() {
    return (
      <React.Fragment>
        <h1>Add Item</h1>
        <AddItem addItem={this.addItem} />
      </React.Fragment>
    );
  }
}
