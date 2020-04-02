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

// az - terrible solution but works for now
function setTags(tags) {
  let tagString = 'tags=' + tags[0];
  for (let i = 1; i < tags.length; i++) {
    tagString = tagString + ',' + tags[i];
  }
  return tagString;
}

export default class Search extends Component {
  state = {
    items: []
  }

  searchItem = (name, tags) => {
    this.setState({items:[]})

    let tagList = "";
    if (tags.length>0){
      tagList = setTags(tags);
    }
    axios.get('/items/search=' + name + '?' + tagList).then(res =>
      res.data.map((item) => {
        this.setState({ items: [...this.state.items, item] })
      })
    );
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
