import React from 'react';
import ReactDOM from 'react-dom';
import GoogleMap from '../components/pages/GoogleMap';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<GoogleMap />, div);
});