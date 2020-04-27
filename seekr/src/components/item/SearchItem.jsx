import React, { Component } from "react";
import PropTypes from "prop-types";
import Checkbox from "./Checkbox";
import GoogleMap from "../pages/GoogleMap";
import ItemTags from "../helper/ItemTags";
import "../../../public/css/Search.css";
import { Form, Button, FormControl, InputGroup } from "react-bootstrap";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSearch } from '@fortawesome/free-solid-svg-icons'

export class SearchItem extends Component {
  componentDidMount = () => {
    // create a set of checked boxes when component is created
    this.selectedCheckboxes = 0;
  };

  state = {
    name: "",
    filter: "Best",
    location: [39.3299, -76.6205],
  };


  callbackFunction = (coordinates) => {
    this.setState({ location: coordinates });
  };

  changeFilter = () => {
    let newFilter = document.getElementById("filters").value
    this.setState({ filter: newFilter });
  }

  toggleCheckbox = (val) => {
    if ((this.selectedCheckboxes & val) === val) {
      this.selectedCheckboxes = this.selectedCheckboxes & ~val;
    } else {
      this.selectedCheckboxes = this.selectedCheckboxes | val;
    }
  };

  createCheckbox = (tag) => (
    <Checkbox
      label={tag.label}
      flagValue={tag.value}
      toggleCheckbox={this.toggleCheckbox}
      key={tag.label}
    />
  );

  createCheckboxes = () => ItemTags.getMapping().map(this.createCheckbox);

  onChange = (e) => {
    if (this.state.name === "") {
      this.props.clearSearch();
    }
    this.setState({ [e.target.name]: e.target.value });
    // if the name is empty, clear the search contents
  };

  onSubmit = (e) => {
    e.preventDefault();
    if (this.state.name === "" && this.state.filter === 'Best') {
      alert("You must enter a search query when sorting by Best Match.");
      return false;
    }
    this.props.searchItem(
      this.state.name,
      this.selectedCheckboxes,
      this.state.filter,
      this.state.location
    ); // call API
    this.setState({ name: "" });
    var boxes = document.getElementsByClassName("box");
    for (let box of boxes) {
      if (box.checked) {
        box.click();
      }
    }
  };

  render() {
    return (
      <div className="search-sidebar">
        <div className="search-sidebar-searchbar">
          <Form onSubmit={this.onSubmit}>
              <InputGroup>
                  <InputGroup.Prepend>
                    <InputGroup.Text>
                      <FontAwesomeIcon icon={faSearch} />
                    </InputGroup.Text>
                  </InputGroup.Prepend>
                  <Form.Control
                    type="text"
                    onChange={this.onChange} 
                    value={this.state.name}
                    placeholder="Search for an item..." 
                    name="name"
                    aria-describedby="inputGroupPrepend"
                  />
              </InputGroup>
            </Form>
          </div>
          <div className="filter-search">
            <div className="checkbox-search">
              <h4>Add Filters</h4>
              {this.createCheckboxes()}
              <div>
              <b>Give a location to search</b>
              </div>
              <div className="googleMap-search">
                <GoogleMap parentCallback={this.callbackFunction} clickable={true}/>
              </div>
            </div>
            <div className="row" style={{ float:"center"}}>
              <label htmlFor="filters" style={{ paddingRight: "5px" }}>
                <h4>Sort by:{" "}</h4>
              </label>
              <select id="filters" onChange={this.changeFilter}>
                <option value="Best">Best Match</option>
                <option value="Recent">Most Recent</option>
                <option value="Proximity">Closest Distance</option>
              </select>
            </div>
          </div>
      </div>
    );
  }
}

SearchItem.propTypes = {
  searchItem: PropTypes.func.isRequired,
};

export default SearchItem;
