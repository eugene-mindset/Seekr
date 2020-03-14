import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Navigation from './components/layout/Navigation';
import About from './components/pages/About';
import Search from './components/pages/Search';
import Add from './components/pages/Add';
import Home from './components/pages/Home';
import Image from 'react-bootstrap/Image'

import './App.css';

class App extends Component {

  render() {
    return (
      <Router>
        <div className="App">
          <Navigation />

          <Route exact path="/" component={Home}/>
          <Route path="/add" component={Add} />
          <Route path="/search" component={Search} />
          <Route path="/about" component={About} />
        </div>
      </Router>
    );
  }
}

export default App;
