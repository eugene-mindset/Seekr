import React, { Component } from 'react';
import axios from 'axios';
import AddItem from '../item/AddItem';
import SubmissionModal from '../item/SubmissionModal';
import Errorpage from './Errorpage';

function getCookieValue(a) {
	let b = document.cookie.match('(^|[^;]+)\\s*' + a + '\\s*=\\s*([^;]+)');
	return b ? b.pop() : null;
}

export default class Add extends Component {
  state = {
    similarItems: [],
    showModal: false,
    submitted: false,
    name: '',
    found: false,
    desc: '',
    location: [39.3299, -76.6205],
    img: [],
    radius: 0,
    tags: 0,
    username: "",
    email: "",
    phone: "",
  };

  resetState = () => {
    this.setState({
      similarItems: [],
      showModal: false,
      submitted: false,
      name: '',
      found: false,
      desc: '',
      location: [39.3299, -76.6205],
      img: [],
      radius: 0,
      tags: 0,
      username: "",
      email: "",
      phone: "",
    });
  }

  submitForm = (name, found, desc, location, tags, img, radius, username, email, phone) => {
    this.setState(
      {
        name: name,
        desc: desc,
        found: found,
        location: location,
        radius: radius,
        tags: tags,
        img: img,
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
    }).then(this.resetState());

    
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
    const userID = getCookieValue("userID");

    if (userID === "null") {
      return (
        <Errorpage></Errorpage>
      )
    }
    
    return (
      <React.Fragment>
        <h1>Add Item</h1><br/>
        <AddItem submitForm={this.submitForm}/>
        <SubmissionModal showModal={this.state.showModal} handleClose={this.closeModal} simItems={this.state.similarItems}/>
      </React.Fragment>
    );
  }
}
