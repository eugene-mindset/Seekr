import React, { Component } from "react";

import Items from "../item/Items";
import axios from "axios";
import SearchItem from "../item/SearchItem";
import CardColumns from "react-bootstrap/CardColumns";
import "../../../public/css/Search.css";
import { trackPromise } from "react-promise-tracker";

function getCookieValue(a) {
	let b = document.cookie.match('(^|[^;]+)\\s*' + a + '\\s*=\\s*([^;]+)');
	return b ? b.pop() : null;
}

export default class Search extends Component {
  componentDidMount() {
    name="%20";
    axios.get("/api/items/timesearch=" + name).then((res) =>
      res.data.map((item) => {
        return this.setState({ items: [...this.state.items, item] });
      })
    );
  }

  state = {
    items: [],
    user_email: ""
  };

  searchItem = (name, tags, filter, location) => {
    this.setState({ items: [] });
    if (filter === "Best") {
      trackPromise(
      axios.get("/api/items/search=" + name + "?tags=" + tags).then((res) =>
        res.data.map((item) => {
          return this.setState({ items: [...this.state.items, item] });
        })
      ));
    } else if (filter === "Recent") {
      // if sort is by recent but query is blank, just search a space, of which
      // the backend will handle by returning all items
      let nameQuery = name.length === 0 ? ' ' : name;
      trackPromise(
      axios.get("/api/items/timesearch=" + nameQuery + "?tags=" + tags).then((res) =>
        res.data.map((item) => {
          return this.setState({ items: [...this.state.items, item] });
        })
      ));
    } else {
      trackPromise(
      axios
        .get(
          "/items/proximitysearch" +
            "?tags=" + tags +
            "&lat=" + location[0] +
            "&lon=" + location[1]
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
    // az - set this to do nothing since when loading search page, already show
    // this.setState({ items: [] });
  };

  deleteItem = (id) => {
    axios.delete(`/api/items/${id}` + "?email=" + getCookieValue("email")).then((res) =>
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
        <CardColumns style={{marginLeft: '350px', display: 'flex', flexWrap: 'wrap'}}>
          <Items items={this.state.items} deleteItem={this.deleteItem} />
        </CardColumns>
      </div>
    );
  }
}
