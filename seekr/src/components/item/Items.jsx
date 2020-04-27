import React, { useContext } from 'react';
import Item from './Item';
import { AuthContext } from "../helper/AuthContext";

import PropTypes from 'prop-types';

const Items = ({items, deleteItem}) => {
  const { name, email } = useContext(AuthContext);

  return items.map((item) => (
    <Item key={item.id} item={item} deleteItem={deleteItem} email={email} user_name={name} />
  ));
};

export default Items;
