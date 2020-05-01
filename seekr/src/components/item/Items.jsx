import React, { useContext } from 'react';
import Item from './Item';
import { AuthContext } from "../helper/AuthContext";


const adminEmails = ['yifanandrew@yahoo.com', 'seekr.oose@gmail.com']

const Items = ({items, deleteItem}) => {

  const { email } = useContext(AuthContext);

  return items.map((item) => (
    <Item key={item.id} item={item} deleteItem={deleteItem} cur_email={email} isAdmin={adminEmails.includes(email)} />
  ));
};

export default Items;
