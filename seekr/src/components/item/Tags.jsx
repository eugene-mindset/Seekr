import React, { Component } from "react";
import "../../App.css";

export default class Tags extends Component {
  getTag = (tag) => <div className="tags">{tag}</div>;

  getTags = () => (
    <div className="tags-container">{this.props.tags.map(this.getTag)}</div>
  );

  render() {
    return this.getTags();
  }
}
