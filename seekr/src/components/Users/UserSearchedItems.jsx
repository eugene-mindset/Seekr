import React, { useState, useContext, useEffect } from "react";
import CardColumns from "react-bootstrap/CardColumns";
import Items from "../item/Items";
import axios from "axios";
import { AuthContext } from "../helper/AuthContext";
import { trackPromise } from "react-promise-tracker";
const columnStyle = {
  display: "flex",
  flexWrap: "wrap",
  justifyContent: "left",
};
function UserSearchedItems() {
  const [items, setItems] = useState([]);
  const { email } = useContext(AuthContext);

  useEffect(() => {
    trackPromise(
      axios
        .get("/api/items/user=" + email)
        .then((result) => setItems(result.data)),
      console.log("done")
    );
  }, [email]);

  const deleteItem = (id) => {
    axios
      .delete(`/api/items/${id}` + "?email=" + getCookieValue("email"))
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

function getCookieValue(a) {
	let b = document.cookie.match('(^|[^;]+)\\s*' + a + '\\s*=\\s*([^;]+)');
	return b ? b.pop() : null;
}

export default UserSearchedItems;
