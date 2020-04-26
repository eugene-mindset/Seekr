import React, { useState, useContext } from "react";
import CardColumns from "react-bootstrap/CardColumns";
import Items from "../item/Items";
import axios from "axios";
import { AuthContext } from "../helper/AuthContext";

const columnStyle = {
  display: "flex",
  flexWrap: "wrap",
  justifyContent: "center",
  marginTop: "70px",
  marginLeft: "10px",
};

function UserSearchedItems() {
  const [items, setItems] = useState([]);
  const { email } = useContext(AuthContext);

  const searchItem = () => {
    setItems([]);
    axios.get("/items/user=" + email).then((res) =>
      res.data.map((item) => {
        setItems((items) => [...items, item]);
      })
    );
	};

	const deleteItem = (id) => {
		axios.delete(`/items/${id}`).then((res) =>
			setItems((items) => [...items.filter((item) => item.id !== id)])
    );
  };

  let onClick = () => {
    searchItem();
  };

  return (
    <div className="user-results">
      <button onClick={onClick}>Click me</button>
      <div>
        Items that you posted:
        <CardColumns style={columnStyle}>
          <Items items={items} deleteItem={deleteItem} />
        </CardColumns>
      </div>
    </div>
  );
}

export default UserSearchedItems;
