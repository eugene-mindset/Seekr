import React from 'react';
import Item from './Item';
import PropTypes from 'prop-types';

class Items extends React.Component {
  render() {
    return this.props.items.map((item) => (
      <Item key={item.id} item={item} markFound={this.props.markFound} deleteItem={this.props.deleteItem}/>
    ));
  }
}

//PropTypes for expected props
Items.propTypes = {
  items: PropTypes.array.isRequired,
  markFound: PropTypes.func.isRequired,
  deleteItem: PropTypes.func.isRequired
}

export default Items;
