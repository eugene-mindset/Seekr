import React, { useContext, useEffect } from 'react';
import Item from './Item';
import { AuthContext } from "../helper/AuthContext";




const Items = ({items, deleteItem}) => {

  const { email, isAdmin } = useContext(AuthContext);
  
  
  console.log(isAdmin)
  
  return items.map((item) => (
    <Item key={item.id} item={item} deleteItem={deleteItem} cur_email={email} isAdmin={isAdmin} />
  ));
};

export default Items;
