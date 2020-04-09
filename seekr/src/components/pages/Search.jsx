import React, { Component } from 'react';

import Items from '../item/Items';
import axios from 'axios';
import SearchItem from '../item/SearchItem';
import CardColumns from 'react-bootstrap/CardColumns'


const columnStyle = {
  display: 'flex',
  flexWrap: 'wrap',
  justifyContent: 'center'
}

export default class Search extends Component {
  state = {
    items: []
  }

  searchItem = (name, tags, filter) => {
    console.log(tags)
    this.setState({items:[]})
    if (filter === 'Best') {
      axios.get('/items/search=' + name + '?tags=' + tags).then(res =>
        res.data.map((item) => {
          this.setState({ items: [...this.state.items, item] })
        })
      );
    } else {
      axios.get('/items/timesearch=' + name + '?tags=' + tags).then(res =>
        res.data.map((item) => {
          this.setState({ items: [...this.state.items, item] })
        })
      );
    }
  }

  deleteItem = (id) => {
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
        <CardColumns style={columnStyle}>
          <Items items={this.state.items} deleteItem={this.deleteItem} />
        </CardColumns>
      </React.Fragment>
    );
  }
}
