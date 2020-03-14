import React from 'react'
import Jumbotron from 'react-bootstrap/Jumbotron'
import Navigation from '../layout/Navigation';

import './stylesheets/Home.css';

export default class Home extends React.Component {
  render() {
    return (
      <div>
        <Jumbotron>
          <h1 className="glow">Seekr: Lost and Found</h1>
          <h2>JHU OOSE Project Spring 2020</h2>
          <p>
            Find and report lost items around campus to help your fellow students!
          </p>
        </Jumbotron>
      </div>
    )
  }
}
