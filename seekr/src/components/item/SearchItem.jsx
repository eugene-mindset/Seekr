import React, { Component } from "react";
import PropTypes from "prop-types";
import Checkbox from "./Checkbox";
import ItemTags from "../helper/ItemTags";

export class SearchItem extends Component {
  componentDidMount = () => {
    // create a set of checked boxes when component is created
    this.selectedCheckboxes = 0;
  };

  state = {
    name: "",
    filter: "Best"
  };

  changeFilter = () => this.setState({filter: document.getElementById("filters").value})

  toggleCheckbox = val => {
    if ((this.selectedCheckboxes & val) === val) {
      this.selectedCheckboxes = this.selectedCheckboxes & ~(val);
    } else {
      this.selectedCheckboxes = this.selectedCheckboxes | val;
    }
  };

  createCheckbox = tag => (
    <Checkbox
      label={tag.label}
      flagValue={tag.value}
      toggleCheckbox={this.toggleCheckbox}
      key={tag.label}
    />
  );

  createCheckboxes = () => ItemTags.getMapping().map(this.createCheckbox);

  onChange = e => this.setState({ [e.target.name]: e.target.value });

  onSubmit = e => {
    e.preventDefault();
    if (this.state.name === "") {
      alert("Item must have a name!");
      return false;
    }
    this.props.searchItem(this.state.name, this.selectedCheckboxes, this.state.filter); // call API

  };

  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-sm-12">
            <form onSubmit={this.onSubmit} style={{ display: "flex" }}>
              <input
                type="text"
                name="name"
                style={{ flex: "10", padding: "5px" }}
                placeholder="Search Item..."
                value={this.state.name}
                onChange={this.onChange}
              />
              <input
                type="submit"
                value="Submit"
                className="btn"
                style={{ flex: "1" }}
              />
            </form>
          </div>
        </div>
        <div style={{ display: "flex" }}>{this.createCheckboxes()}</div>
        <div style={{ display: "flex" }}>
          <label for="filters">Sort by:  </label>
          <select id="filters" onChange={this.changeFilter}>
            <option value="Best">Best match</option>
            <option value="Recent">Most Recent</option>
          </select>
        </div>
      </div>
    );
  }
}

SearchItem.propTypes = {
  searchItem: PropTypes.func.isRequired
};

export default SearchItem;
