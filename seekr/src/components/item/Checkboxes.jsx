import React, { Component } from "react";
import Checkbox from "./Checkbox";

// DEPRECATED
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
      toggleCheckbox={this.props.toggleCheckbox}
      checkedState={this.props.selectedCheckboxes.includes(label) ? true : false}
      key={label}
    />
  );

  createCheckboxes = () => tags.map(this.createCheckbox);

  render() {
    return <div style={{ display: "flex" }}>{this.createCheckboxes()}</div>;
  }
}

export default Checkboxes;