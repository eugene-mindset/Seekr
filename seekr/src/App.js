import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Navigation from './components/layout/Navigation';
import Search from './components/pages/Search';
import Add from './components/pages/Add';

import './App.css';

class App extends Component {
  state = {
    loading: true
  };

  componentDidMount() {
    demoAsyncCall().then(() => this.setState({ loading: false }));
  }

  render() {
    const { loading } = this.state;

    if(loading) {
      return null;
    }

    return (
      <Router>
        <div className="App">
          <Navigation />
          <Route exact path="/" component={Search}/>
          <div className="site-container">
            <Route path="/add" component={Add} />
          </div>
        </div>
      </Router>
    );
  }
}

function demoAsyncCall() {
  return new Promise((resolve) => setTimeout(() => resolve(), 2500));
}

export default App;
