import React, { Component } from 'react';
import PropTypes from 'prop-types';


export class SearchItem extends Component {
    state = {
        name: ''
    }

    onChange = (e) => this.setState({ [e.target.name]: e.target.value });

    onSubmit = (e) => {
        e.preventDefault();
        this.props.searchItem(this.state.name); // searchItem has a searchItem property that shows what item name is to be queried
    }

    render() {
        return (
            // flexbox
            <form onSubmit={this.onSubmit} style={{ display: 'flex' }}>
                <input
                    type="text"
                    name="name"
                    style={{ flex: '10', padding: '5px' }}
                    placeholder="Search Item..."
                    value={this.state.name}
                    onChange={this.onChange}
                />
                <input
                    type="submit"
                    value="Submit"
                    className="btn"
                    style={{ flex: '1' }}
                />
            </form>
        )
    }
}


SearchItem.propTypes = {
    searchItem: PropTypes.func.isRequired
}

export default SearchItem
