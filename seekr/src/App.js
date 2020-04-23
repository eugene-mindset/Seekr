import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Navigation from './components/layout/Navigation';
import About from './components/pages/About';
import Search from './components/pages/Search';
import Add from './components/pages/Add';
import Facebook from './FacebookLogin'; 

import './App.css';
import FacebookLogin from './FacebookLogin';

class App extends Component {

  render() {
    return (
      <Router>
        <div className="App">
          <Navigation />
          <Route exact path="/" component={Search}/>
          <div className="site-container">
            <Route path="/add" component={Add} />
            <Route path="/about" component={About} />
            <Route path="/user-login" component={Facebook} />
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
