import React, { Component } from 'react';
import { BrowserRouter as Router, Route} from 'react-router-dom';

import Header from './components/layout/Header';
import Items from './components/Items';
import AddItem from './components/AddItem';
import About from './components/pages/About';
import uuid from 'uuid';

import './App.css';

class App extends Component {
  state = {
    items: [
      {
        id: uuid.v4(),
        name: 'Test',
        found: false
      },
      {
        id: uuid.v4(),
        name: 'Test2',
        found: false
      },

    ]
  }

  // Toggle state vars
  // Arrow function vs using .bind() for props
  markFound = (id) => {
    this.setState({ items: this.state.items.map(item => {
      if(item.id === id){
        item.found = !item.found
      }
      return item;
    }) });
  }

  deleteItem = (id) => {
      // ...spread operator to get list of items make a copy
      // filter out all tha arent the item to remove the item, this is only front end so non persisting
      this.setState({ items: [...this.state.items.filter(item => item.id !== id)]  })
  }

  addItem = (name) => {
    const newItem = {
      id: uuid.v4(),
      name: name,
      found: false
    }
    this.setState({ items: [...this.state.items, newItem] })
  }

  render() {
    return (
      <Router>
        <div className="App">
          <div className="container">
            <Header />
            <Route exact path="/" render={props => (
              <React.Fragment>
                <AddItem addItem={this.addItem} />
                <Items items={this.state.items} markFound={this.markFound} deleteItem={this.deleteItem}/>
              </React.Fragment>
            )} />
            <Route path="/about" component={About} />
          </div>      
        </div>
      </Router>
    );
  }
}

export default App;
