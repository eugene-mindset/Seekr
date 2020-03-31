import React, { Component } from "react";
import PropTypes from "prop-types";
import Checkbox from "./Checkbox";
import Checkboxes from "./Checkboxes";


export class SearchItem extends Component {
  state = {
    name: ""
  };

  onChange = e => this.setState({ [e.target.name]: e.target.value });

  onSubmit = e => {
    e.preventDefault();
    // searchItem has a searchItem property which is a function in the parent component
    this.props.searchItem(this.state.name); // also send the checkboxes
    for (const checkbox of this.selectedCheckboxes) {
      console.log(checkbox, " is selected.");
    }
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
        <Checkboxes />
      </div>

    );
  }
}

SearchItem.propTypes = {
  searchItem: PropTypes.func.isRequired
};

export default SearchItem;
