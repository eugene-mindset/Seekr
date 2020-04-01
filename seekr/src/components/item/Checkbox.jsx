import React, { Component } from "react";
import PropTypes from "prop-types";

class Checkbox extends Component {
  state = {
    isChecked: false
  };

  toggleCheckboxChange = () => {
    const { toggleCheckbox, label } = this.props;

    this.setState(({ isChecked }) => ({
      isChecked: !isChecked
    }));

    toggleCheckbox(label);
  };


  render() {
    const { label } = this.props;
    const { isChecked } = this.state;

    return (
      <div className="checkbox" style={{ marginRight: "10px" }}>
        <label>
          <input
            type="checkbox"
            value={label}
            checked={isChecked}
            onChange={this.toggleCheckboxChange}
          />

          {label}
        </label>
      </div>
    );
  }
}

Checkbox.propTypes = {
  label: PropTypes.string.isRequired,
  toggleCheckbox: PropTypes.func.isRequired
};

export default Checkbox;
