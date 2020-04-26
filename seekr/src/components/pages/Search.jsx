import React, { Component } from "react";

import Items from "../item/Items";
import Modal from "../item/Modal";
import axios from "axios";
import SearchItem from "../item/SearchItem";
import CardColumns from "react-bootstrap/CardColumns";
import "../../../public/css/Search.css";

const columnStyle = {
  display: "flex",
  flexWrap: "wrap",
  justifyContent: "center",
  marginTop: "70px",
  marginLeft: "10px"

};

export default class Search extends Component {
  state = {
    items: [],
    isShowing: false
  };

  openModalHandler = () => {
    this.setState({
        isShowing: true
    });
  }

  closeModalHandler = () => {
    this.setState({
        isShowing: false
    });
  }

  searchItem = (name, tags, filter, location) => {
    this.setState({ items: [] });
    if (filter === "Best") {
      axios.get("/items/search=" + name + "?tags=" + tags).then((res) =>
        res.data.map((item) => {
          return this.setState({ items: [...this.state.items, item] });
        })
      );
    } else if (filter === "Recent") {
      axios.get("/items/timesearch=" + name + "?tags=" + tags).then((res) =>
        res.data.map((item) => {
          return this.setState({ items: [...this.state.items, item] });
        })
      );
    } else {
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
        );
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
      <React.Fragment>
        <div className="search-sidebar">
          <SearchItem
            searchItem={this.searchItem}
            clearSearch={this.clearSearch}
          />
        </div>

        <br />
        <div className="results" onClick={() => this.openModalHandler()}>
          <CardColumns style={columnStyle} >
            <Items items={this.state.items} deleteItem={this.deleteItem}/>
          </CardColumns>
        </div>

        <div>
            { this.state.isShowing ? <div onClick={this.closeModalHandler} className="back-drop"></div> : null }

            

            <Modal
                className="modal"
                show={this.state.isShowing}
                close={this.closeModalHandler}>
                    Maybe aircrafts fly very high because they don't want to be seen in plane sight?
            </Modal>
        </div>
      </React.Fragment>
    );
  }
}
