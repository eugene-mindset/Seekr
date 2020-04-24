import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Navigation from './components/layout/Navigation';
import About from './components/pages/About';
import Search from './components/pages/Search';
import Add from './components/pages/Add';
import Facebook from './components/Users/Facebook';
import ProtectedRoute from './ProtectedRoute';


import './App.css';
import FacebookLogin from './components/Users/Facebook';

class App extends Component {

  state = {
    user: false
  }
  callbackFunction = (isLoggedIn) => {
    this.setState({user: isLoggedIn})
  }

  render() {
    return (
      <Router>
        <div className="App">
          <Navigation />
          <Route exact path="/" component={Search}/>
          <div className="site-container">
            <Route path="/add" component={Add} />
            <Route path="/about" component={About} />
            <Facebook parentCallback={this.callbackFunction}/>
            <ProtectedRoute exact path='/user-login' user={this.user} component={About} />
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
