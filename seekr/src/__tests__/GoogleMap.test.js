import React from 'react';
import ReactDOM from 'react-dom';
import { render, unmountComponentAtNode } from "react-dom";
import { act } from "react-dom/test-utils";
import GoogleMap from '../components/pages/GoogleMap';

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
  ReactDOM.render(<GoogleMap clickable={false}/>, div);
});

it("renders with or without a location", () => {
    act(() => {
      render(<GoogleMap clickable={false}/>, container);
    });
    

    act(() => {
      render(<GoogleMap clickable={false} loc={{lat: 39.2299, lng: -76.6205}} />, container);
    });
    
  });