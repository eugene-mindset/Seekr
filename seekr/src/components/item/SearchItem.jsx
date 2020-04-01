import React, { Component } from "react";
import PropTypes from "prop-types";
import Checkboxes from "./Checkboxes";

export class SearchItem extends Component {
  componentDidMount = () => {
    // create a set of checked boxes when component is created
    this.selectedCheckboxes = new Set();
  };

  state = {
    name: ""
  };

  toggleCheckbox = label => {
    if (this.selectedCheckboxes.has(label)) {
      this.selectedCheckboxes.delete(label);
    } else {
      this.selectedCheckboxes.add(label);
    }
  };

  onChange = e => this.setState({ [e.target.name]: e.target.value });

  onSubmit = e => {
    e.preventDefault();
    if (this.state.name === "") {
      alert("Item must have a name!");
      return false;
    }
    this.props.searchItem(this.state.name, Array.from(this.selectedCheckboxes));
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
        <Checkboxes toggleCheckbox={this.toggleCheckbox} />
      </div>
    );
  }
}

SearchItem.propTypes = {
  searchItem: PropTypes.func.isRequired
};

export default SearchItem;
