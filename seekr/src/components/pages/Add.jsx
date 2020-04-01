import React, { Component } from 'react';
import axios from 'axios';
import AddItem from '../item/AddItem';

export default class Add extends Component {
    
  addItem = (name, found, desc, location, tags) => {
    axios.post('/items', {
      name: name,
      found: found,
      desc: desc,
      location: location,
      tags: tags
    })
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
