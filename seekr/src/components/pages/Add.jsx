import React, { Component } from 'react';
import axios from 'axios';
import AddItem from '../item/AddItem';

export default class Add extends Component {

  addItem = (name, found, desc, location, tags, img, radius, username, email, phone) => {
    var data = new FormData();
    data.append('name', name);
    data.append('desc', desc);
    data.append('found', found);
    data.append('latitude', location[0]);
    data.append('longitude', location[1]);
    data.append('radius', radius);
    data.append('tags', tags);
    data.append('username', username);
    data.append('email', email);
    data.append('phone', phone);
    img.forEach(i => {
      // Append multiple files to request form
      data.append('image', i);
    });

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
        <h1>Add an Item</h1>
        <br/>
        <AddItem addItem={this.addItem} />
      </React.Fragment>
    );
  }
}
