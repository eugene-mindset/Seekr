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

export class Checkboxes extends Component {
  createCheckbox = label => (
    <Checkbox
      label={label}
      handleCheckboxChange={this.props.toggleCheckbox}
      key={label}
    />
  );

  createCheckboxes = () => tags.map(this.createCheckbox);

  render() {
    return <div style={{ display: "flex" }}>{this.createCheckboxes()}</div>;
  }
}

export default Checkboxes;