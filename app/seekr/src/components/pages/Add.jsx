import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import axios from 'axios';
import AddItem from '../item/AddItem';

export default class Add extends React.Component {
      // Toggle state vars
      // Arrow function vs using .bind() for props
      markFound = (id) => {
        const item = this.state.items.filter(item => { return item.id === id })[0];
    
        axios.put(`/items/${id}`, {
          name: item.name,
          found: !item.found
        }).then(res =>
          this.setState({
            items:
              this.state.items.map(item => {
                if (item.id === id) {
                  item.found = !item.found
                }
                return item;
              })
          })
        );
      }
    
      addItem = (name, found, desc) => {
        axios.post('/items', {
          name: name,
          found: found,
          desc: desc
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