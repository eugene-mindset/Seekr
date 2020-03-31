import React, { Component } from "react";
// import PropTypes from "prop-types";
import Checkbox from "./Checkbox";

const tags = [
  "tech",
  "clothing",
  "jewelry",
  "pet",
  "personal",
  "apparel",
  "other"
];

// TODO: figure out how to use props to pass selectedCheckboxes up to SearchItem
export class Checkboxes extends Component {
  componentDidMount = () => {
    // create a set of checked boxes when component is created
    this.selectedCheckboxes = new Set();
  };

  toggleCheckbox = label => {
    if (this.selectedCheckboxes.has(label)) {
      this.selectedCheckboxes.delete(label);
    } else {
      this.selectedCheckboxes.add(label);
    }
  };

  createCheckbox = label => (
    <Checkbox
      label={"  " + label + "  "}
      handleCheckboxChange={this.toggleCheckbox}
      key={label}
    />
  );

  createCheckboxes = () => tags.map(this.createCheckbox);

  render() {
    return <div style={{ display: "flex" }}>{this.createCheckboxes()}</div>;
  }
}

export default Checkboxes;