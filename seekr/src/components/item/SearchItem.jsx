import React, { Component } from "react";
import PropTypes from "prop-types";
import Checkbox from "./Checkbox";
import GoogleMap from "../pages/GoogleMap";
import ItemTags from "../helper/ItemTags";
import "../../../public/css/Search.css";

export class SearchItem extends Component {
  componentDidMount = () => {
    // create a set of checked boxes when component is created
    this.selectedCheckboxes = 0;
  };

  state = {
    name: "",
    filter: "Best",
    location: [39.3299, -76.6205],
  };


  callbackFunction = (coordinates) => {
    this.setState({ location: coordinates });
  };

  changeFilter = () =>
    this.setState({ filter: document.getElementById("filters").value });

  toggleCheckbox = (val) => {
    if ((this.selectedCheckboxes & val) === val) {
      this.selectedCheckboxes = this.selectedCheckboxes & ~val;
    } else {
      this.selectedCheckboxes = this.selectedCheckboxes | val;
    }
  };

  createCheckbox = (tag) => (
    <Checkbox
      label={tag.label}
      flagValue={tag.value}
      toggleCheckbox={this.toggleCheckbox}
      key={tag.label}
    />
  );

  createCheckboxes = () => ItemTags.getMapping().map(this.createCheckbox);

  onChange = (e) => {
    if (this.state.name === "") {
      this.props.clearSearch();
    }
    this.setState({ [e.target.name]: e.target.value });
    // if the name is empty, clear the search contents
  };

  onSubmit = (e) => {
    e.preventDefault();
    if (this.state.name === "") {
      alert("Item must have a name!");
      return false;
    }
    this.props.searchItem(
      this.state.name,
      this.selectedCheckboxes,
      this.state.filter,
      this.state.location
    ); // call API
    this.setState({ name: "" });
    var boxes = document.getElementsByClassName("box");
    for (let box of boxes) {
      if (box.checked) {
        box.click();
      }
    }
  };

  render() {
    return (
      <div
        className="container"
        style={{
          maxWidth: "450px",
          alignItems: "start",
          marginTop: "70px",
          marginLeft: "15px"
        }}
      >
        <h1 align="left">Search for an item</h1>

        <div className="row">
          <div className="col" style={{ paddingLeft: "5px" }}>
            <form onSubmit={this.onSubmit} style={{ display: "flex" }}>
              <input
                type="text"
                name="name"
                style={{ flex: "7", padding: "5px" }}
                placeholder="Search Item..."
                value={this.state.name}
                onChange={this.onChange}
              />
              <input
                type="submit"
                value="Search"
                className="btn"
                style={{ flex: "1", fontWeight: "bold" }}
              />
            </form>
          </div>
        </div>
        <div className="row">
          <div style={{ display: "flex", paddingLeft: "5px" }}>
            {this.createCheckboxes()}
          </div>
        </div>
        <div
          className="row"
          style={{
            display: "flex",
            paddingLeft: "5px",
            alignItems: "baseline",
          }}
        >
          <label htmlFor="filters" style={{ paddingRight: "5px" }}>
            Sort by:{" "}
          </label>
          <select id="filters" onChange={this.changeFilter}>
            <option value="Best">Best Match</option>
            <option value="Recent">Most Recent</option>
            <option value="Proximity">Closest Distance</option>
          </select>
        </div>
        <div className="row" style={{ paddingLeft: "5px" }}>
          Supply a location to find nearby items.
        </div>
        <div className="row" style={{ paddingLeft: "5px" }}>
          <GoogleMap parentCallback={this.callbackFunction} />
        </div>
      </div>
    );
  }
}

SearchItem.propTypes = {
  searchItem: PropTypes.func.isRequired,
};

export default SearchItem;
