import React, { Component } from "react";

import Items from "../item/Items";
import axios from "axios";
import SearchItem from "../item/SearchItem";
import CardColumns from "react-bootstrap/CardColumns";
import "../../../public/css/Search.css";
import { trackPromise } from "react-promise-tracker";

export default class Search extends Component {
  state = {
    items: []
  };

  searchItem = (name, tags, filter, location) => {
    this.setState({ items: [] });
    if (filter === "Best") {
      trackPromise(
      axios.get("/items/search=" + name + "?tags=" + tags).then((res) =>
        res.data.map((item) => {
          return this.setState({ items: [...this.state.items, item] });
        })
      ));
    } else if (filter === "Recent") {
      trackPromise(
      axios.get("/items/timesearch=" + name + "?tags=" + tags).then((res) =>
        res.data.map((item) => {
          return this.setState({ items: [...this.state.items, item] });
        })
      ));
    } else {
      trackPromise(
      axios
        .get(
          "/items/proximitysearch=" +
            name +
            "?tags=" +
            tags +
            "&lat=" +
            location[0] +
            "&lon=" +
            location[1]
        )
        .then((res) =>
          res.data.map((item) => {
            return this.setState({ items: [...this.state.items, item] });
          })
        ));
    }
  };

  // call this function if the search bar is empty
  clearSearch = () => {
    this.setState({ items: [] });
  };

  deleteItem = (id) => {
    axios.delete(`/items/${id}`).then((res) =>
      this.setState({
        items: [...this.state.items.filter((item) => item.id !== id)],
      })
    );
  };

  render() {
    return (
      <div className="searchComponent">
        <SearchItem
          searchItem={this.searchItem}
          clearSearch={this.clearSearch}
        />
        <div style={{marginLeft: "450px", float:"left"}}>
          <CardColumns>
            <Items items={this.state.items} deleteItem={this.deleteItem} />
          </CardColumns>
        </div>
      </div>
    );
  }
}
