import React from 'react';
import ReactDOM from 'react-dom';
import { render, unmountComponentAtNode } from "react-dom";
import SearchItem from '../components/item/SearchItem';

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
  function searchItem() {
    alert('test');
  }

  ReactDOM.render(<SearchItem searchItem={() => searchItem()}/>, div);
});