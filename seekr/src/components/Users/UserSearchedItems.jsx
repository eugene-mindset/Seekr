import React, { useState, useContext, useEffect } from "react";
import CardColumns from "react-bootstrap/CardColumns";
import Items from "../item/Items";
import axios from "axios";
import { AuthContext } from "../helper/AuthContext";

const columnStyle = {
  display: "flex",
  flexWrap: "wrap",
  justifyContent: "left",
};

function UserSearchedItems() {
  const [items, setItems] = useState([]);
  const { email } = useContext(AuthContext);

  useEffect(() => {
    const fetchData = async () => {
      const result = await axios.get("/api/items/user=" + email);
      setItems(result.data);
    };
    fetchData();
    console.log("done");
  }, []);

  const deleteItem = (id) => {
    axios
      .delete(`/api/items/${id}`)
      .then((res) =>
        setItems((items) => [...items.filter((item) => item.id !== id)])
      );
  };


  return (
    <div className="user-results">
      <div>
        <i>Items that you posted:</i>
        <CardColumns style={columnStyle}>
          <Items items={items} deleteItem={deleteItem} />
        </CardColumns>
      </div>
    </div>
  );
}

export default UserSearchedItems;
