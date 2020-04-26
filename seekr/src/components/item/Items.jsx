import React, { useContext } from 'react';
import Item from './Item';
import { AuthContext } from "../helper/AuthContext";

import PropTypes from 'prop-types';

// class Items extends React.Component {
//   render() {
//     return this.props.items.map((item) => (
//       <Item key={item.id} item={item} deleteItem={this.props.deleteItem}/>
//     ));
//   }
// }

// //PropTypes for expected props
// Items.propTypes = {
//   items: PropTypes.array.isRequired,
//   deleteItem: PropTypes.func.isRequired
// }

const Items = ({items, deleteItem}) => {
  const { email } = useContext(AuthContext);

  return items.map((item) => (
    <Item key={item.id} item={item} deleteItem={deleteItem} email={email} />
  ));
};

export default Items;
