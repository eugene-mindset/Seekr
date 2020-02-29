import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Items from '../item/Items';
import axios from 'axios';
import AddItem from '../item/AddItem';

export default class Add extends React.Component {
    state = {
        items: []
    }

    componentDidMount() {
        axios.get('/items')
          .then(res =>
            this.setState({ items: res.data })
          );
      }
    
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
    
      deleteItem = (id) => {
        // ...spread operator to get list of items make a copy
        // filter out all tha arent the item to remove the item, this is only front end so non persisting
        axios.delete(`/items/${id}`)
          .then(res => this.setState({
            items: [...this.state.items.filter
              (item => item.id !== id)]
          })
          );
      }
    
      addItem = (name, found, desc) => {
        axios.post('/items', {
          name: name,
          found: found,
          desc: desc
        }).then(res =>
          this.setState({ items: [...this.state.items, res.data] })
        );
      }

      render() {
        return (
            <React.Fragment>
                <h1>Add Item</h1>
                <AddItem addItem={this.addItem} />  
                <Items items={this.state.items} markFound={this.markFound} deleteItem={this.deleteItem} />
            </React.Fragment>
        );
    }

}