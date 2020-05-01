import React from 'react';
import ReactDOM from 'react-dom';
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import AddItem from '../components/item/AddItem';

state = {
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

  //ReactDOM.render(<AddItem clickable={false}/>, div);
});