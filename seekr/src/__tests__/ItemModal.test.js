import React from 'react';
import ReactDOM from 'react-dom';
import { render, unmountComponentAtNode } from "react-dom";
import ItemModal from '../components/item/ItemModal';


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
  function handleClose() {
    alert('test');
  }
  let id = '';
  let name='';
  let found=false;
  let images=[];
  let timestamp=0;
  let tags='';
  let email='';
  let location=[0, 0]

  ReactDOM.render(<ItemModal showModal={true} handleClose={() => handleClose()} itemData={{id, name, found, images, timestamp, tags, email, location}}/>, div);
});