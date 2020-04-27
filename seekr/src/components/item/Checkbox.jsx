import React, { Component } from "react";
import PropTypes from "prop-types";
import "../../../public/css/Checkbox.css";

class Checkbox extends Component {
  state = {
    isChecked: false
  };

  toggleCheckboxChange = () => {
    const { toggleCheckbox, flagValue } = this.props;

    this.setState(({ isChecked }) => ({
      isChecked: !isChecked
    }));

    toggleCheckbox(flagValue);
  };


  render() {
    const { label } = this.props;
    const { isChecked } = this.state;

    return (
      <div className="checkbox">
        <label className="checkbox-label">
          {label}
        </label>
          <input className="box"
            type="checkbox"
            value={label}
            checked={isChecked}
            onChange={this.toggleCheckboxChange}
          />

      </div>
    );
  }
}

Checkbox.propTypes = {
  label: PropTypes.string.isRequired,
  flagValue: PropTypes.number.isRequired,
  toggleCheckbox: PropTypes.func.isRequired
};

export default Checkbox;
