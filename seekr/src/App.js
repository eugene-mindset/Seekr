import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Navigation from './components/layout/Navigation';
import About from './components/pages/About';
import Search from './components/pages/Search';
import Add from './components/pages/Add';

import './App.css';

class App extends Component {

  render() {
    return (
      <Router>
        <div className="App">
          <Navigation />
          
          <div className="site-container">
            <Route path="/search" component={Search}/>
            <Route path="/add" component={Add} />
            <Route path="/about" component={About} />
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
