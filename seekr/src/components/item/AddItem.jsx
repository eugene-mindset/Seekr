import React, { Component } from 'react'
import PropTypes from 'prop-types';
import GoogleMap from '../pages/GoogleMap';
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

export class AddItem extends Component {
  componentDidMount = () => {
    // create a set of checked boxes when component is created
    this.selectedCheckboxes = new Set();
  };

  state = {
    name: '',
    found: false,
    desc: '',
    location: [39.3299, -76.6205],
    img: ''
  }

  // idea: make checkboxes as a state that keeps track of checked or not
  // would need to modify for SearchItem as well
  
  toggleCheckbox = label => {
    if (this.selectedCheckboxes.has(label)) {
      this.selectedCheckboxes.delete(label);
    } else {
      this.selectedCheckboxes.add(label);
    }
  };

  createCheckbox = label => (
    <Checkbox
      label={label}
      toggleCheckbox={this.toggleCheckbox}
      key={label}
    />
  );


  createCheckboxes = () => tags.map(this.createCheckbox);
  
  uncheckCheckboxes = () => tags.map(this.createCheckbox);

  callbackFunction = (coordinates) => {
    this.setState({location: coordinates})
  }

  onClick = (e) => {
    this.setState({found: true});
  }

  onSubmit = (e) => {
    e.preventDefault();
    if (this.state.name === '') {
      alert("Item must have a name!");
      return false;
    }

    this.props.addItem(this.state.name, this.state.found, this.state.desc, this.state.location, Array.from(this.selectedCheckboxes), this.state.img);
    this.setState({ name: '', found: false, desc: '', location: [39.3299, -76.6205], img: ''});
    document.getElementById("imageUpload").value = "";
  }

  onChange = (e) => this.setState({ [e.target.name]: e.target.value });

  fileSelectedHandler = (e) => {
    this.setState({
      img: e.target.files[0]
    })
  }

  render() {
    return (
      // flexbox
      <div>
        <form onSubmit={this.onSubmit} style={{ display: 'flex' }}>
          <input
            type="text"
            name="name"
            style={{ flex: '10', padding: '5px' }}
            placeholder="Add Item Name..."
            value={this.state.name}
            onChange={this.onChange}
          />
          <input
            type="text"
            name="desc"
            style={{ flex: '10', padding: '5px' }}
            placeholder="Add Item Description..."
            value={this.state.desc}
            onChange={this.onChange}
          />
          <input
            type="file"
            id="imageUpload"
            onChange={this.fileSelectedHandler}
          />
          <input
            type="submit"
            value="List as Missing"
            className="btn"
            style={{ flex: '1' }}
          />
          <input
            type="submit"
            value="List as Found"
            className="btn"
            style={{ flex: '1' }}
            onClick={this.onClick}
          />
        </form>
        <div style={{ display: "flex" }}>{this.createCheckboxes()}</div>
        <GoogleMap parentCallback={this.callbackFunction}/>
      </div>
    )
  }
}

AddItem.propTypes = {
  addItem: PropTypes.func.isRequired
}

export default AddItem;