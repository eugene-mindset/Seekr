import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Items from './components/item/Items';
import axios from 'axios';
import SearchItem from './components/item/SearchItem';

import './App.css';


export default class Search extends React.Component {
    state = {
        items: []
    }

    // componentDidMount() {
    //     axios.get('/items')
    //         .then(res =>
    //             this.setState({ items: res.data })
    //         );
    // }

    markFound = (id) => {
        const item = this.state.items.filter(item => { return item.id === id })[0];

        axios.put(`/items/${id}`, {
            name: item.name,
            found: !item.found
        }).then(res =>
            this.setState({
                items:
                    this.state.items.map(item => {
                        if (item.id === id) {
                            item.found = !item.found
                        }
                        return item;
                    })
            })
        );
    }

    searchItem = (name) => {
        axios.get('/items/' + name).then(res =>
            this.setState({ items: [res.data] })
            // {console.log(res.data);}
        );
    }

    deleteItem = (id) => {
        // ...spread operator to get list of items make a copy
        // filter out all tha arent the item to remove the item, this is only front end so non persisting
        axios.delete(`/items/${id}`)
            .then(res => this.setState({
                items: [...this.state.items.filter
                    (item => item.id !== id)]
            })
        );
    }


    render() {
        return (
            <React.Fragment>
                <h1>Search</h1>
                <SearchItem searchItem={this.searchItem} />
                <Items items={this.state.items} markFound={this.markFound} deleteItem={this.deleteItem} />
            </React.Fragment>
        );
    }


}

