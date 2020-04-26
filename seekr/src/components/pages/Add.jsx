import React, { Component } from 'react';
import axios from 'axios';
import AddItem from '../item/AddItem';
import SubmissionModal from '../item/SubmissionModal';

export default class Add extends Component {
  state = {
    similarItems: [],
    showModal: false,
    submit: false,
    name: '',
    found: false,
    desc: '',
    location: [39.3299, -76.6205],
    img: [],
    radius: 0,
    username: "",
    email: "",
    phone: "",
  };

  submitForm = (name, found, desc, location, tags, img, radius, username, email, phone) => {
    this.setState(
      {
        name: name,
        found: found,
        desc: desc,
        location: location,
        img: img,
        radius: radius,
        username: username,
        email: email,
        phone: phone
      }
    )

    axios.get(
      "/sim_items" +
        "?name=" + name +
        "&desc=" + desc +
        "&tags=" + tags +
        "&found=" + found +
        "&lat=" + location[0] +
        "&long=" + location[1] +
        "&radius=" + radius
    ).then(
      (res) => {
        res.data.map((item) => {
          return this.setState({ similarItems: [...this.state.similarItems, item] });
        });

        if (this.state.similarItems.length > 0) {
          this.setState({showModal: true});
        } else {
          this.addItem(name, found, desc, location, tags, img, radius, username, email, phone);
        }
      }
    );
  }

  addItem = () => {
    var data = new FormData();
    data.append('name', this.state.name);
    data.append('desc', this.state.desc);
    data.append('found', this.state.found);
    data.append('latitude', this.state.location[0]);
    data.append('longitude', this.state.location[1]);
    data.append('radius', this.state.radius);
    data.append('tags', this.state.tags);
    data.append('username', this.state.username);
    data.append('email', this.state.email);
    data.append('phone', this.state.phone);
    this.state.img.forEach(i => {
      // Append multiple files to request form
      data.append('image', i);
    });

    axios({
      method: 'post',
      url: '/items',
      data: data,
      headers: {'Content-Type': 'multipart/form-data' }
      });
  }

  closeModal = (doSubmit) => {
    if (doSubmit) {
      this.setState({submit: true});
      this.addItem();
    }

    this.setState({similarItems: []});
    this.setState({showModal: false});
  }

  render() {
    return (
      <React.Fragment>
        <h1>Add Item</h1>
        <AddItem addItem={this.submitForm} submitted={this.state.submit} />
        <SubmissionModal showModal={this.state.showModal} handleClose={this.closeModal} simItems={this.state.similarItems}/>
      </React.Fragment>
    );
  }
}
