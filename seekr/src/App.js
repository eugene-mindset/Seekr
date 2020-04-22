import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Navigation from './components/layout/Navigation';
import About from './components/pages/About';
import Search from './components/pages/Search';
import Add from './components/pages/Add';
import UserInfo from './components/pages/UserInfo';

import './App.css';

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
            <Route path="/userinfo" component={UserInfo} />
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
