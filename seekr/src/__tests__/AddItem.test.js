import React from 'react';
import ReactDOM from 'react-dom';
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import AddItem from '../components/item/AddItem';

let container = null;
beforeEach(() => {
  // setup a DOM element as a render target
  container = document.createElement("div");
  document.body.appendChild(container);
});

afterEach(() => {
  // cleanup on exiting
  unmountComponentAtNode(container);
  container.remove();
  container = null;
});

it('renders without crashing', () => {
  const div = document.createElement('div');
  const state = {
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

  submitForm = (name, found, desc, location, tags, img, radius, username, email, phone) => {
    state.name=name
    state.desc=desc
    state.found=found
    state.location=location
    state.radius=radius
    state.tags=tags
    state.img=img
    state.username=username
    state.email=email
    state.phone=phone
  }

  ReactDOM.render(<AddItem submitForm={submitForm}/>, div);
});