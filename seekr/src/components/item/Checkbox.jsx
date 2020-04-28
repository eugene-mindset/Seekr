import React, { Component } from "react";
import PropTypes from "prop-types";

class Checkbox extends Component {
  state = {
    isChecked: false
  };

  toggleCheckboxChange = () => {
    const { toggleCheckbox, flagValue, getState } = this.props;

    this.setState(({ isChecked }) => ({
      isChecked: !isChecked
    }));

    toggleCheckbox(flagValue);
    getState(this.state.isChecked); // set getState to the value of isChecked
  };


  render() {
    const { label } = this.props;
    const { isChecked } = this.state;

    return (
      <div className="checkbox">
        <label className="checkbox-label">
          <input className="box"
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
