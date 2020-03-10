import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Header from './components/layout/Header';
import Items from './components/item/Items';
import AddItem from './components/item/AddItem';
import About from './components/pages/About';
import axios from 'axios';
import Search from './components/pages/Search';
import Add from './components/pages/Add';
import GoogleMap from './components/pages/GoogleMap'

import './App.css';

class App extends Component {
  state = {
    items: []
  }

  


  render() {
    return (
      <Router>
        <div className="App">
          <div className="container">
            <Header />
            {/* Add item */}
            <Route path="/add" component={Add} />

            {/* Search item */}
            <Route path="/search" component={Search} />

            <Route path="/about" component={About} />

            <Route path ="/Map" component={GoogleMap} />

            <Route exact path="/" render={props => (
              <React.Fragment>
                <h1>Click on tabs to choose correct path</h1>
                <Items items={this.state.items} markFound={this.markFound} deleteItem={this.deleteItem} />
              </React.Fragment>
            )}/>
          </div>
        </div>
      </Router>
    );
  }
}

export default App;
