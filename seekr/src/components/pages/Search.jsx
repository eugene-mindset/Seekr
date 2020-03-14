import React, { Component } from 'react';

import Items from '../item/Items';
import axios from 'axios';
import SearchItem from '../item/SearchItem';
import CardColumns from 'react-bootstrap/CardColumns'


export default class Search extends Component {
  state = {
    items: []
  }

  searchItem = (name) => {
    this.setState({items:[]})
    axios.get('/items/search=' + name).then(res =>
      res.data.map((item) => {
        this.setState({ items: [...this.state.items, item] })
      })
    );
  }

  deleteItem = (id) => {
    // ...spread operator to get list of items make a copy
    // filter out all tha arent the item to remove the item, this is only front end so non persisting
    axios.delete(`/items/${id}`)
      .then(res => this.setState({
        items: [...this.state.items.filter(item => item.id !== id)]
      })
    );
  }

  render() {
    return (
      <React.Fragment>
        <h1>Search</h1>
        <SearchItem searchItem={this.searchItem} />
        <br />
        <CardColumns>
          <Items items={this.state.items} deleteItem={this.deleteItem} />
        </CardColumns>
      </React.Fragment>
    );
  }
}
