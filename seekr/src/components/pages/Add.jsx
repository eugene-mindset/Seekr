import React, { Component, useContext } from "react";
import axios from "axios";
import AddItem from "../item/AddItem";
import { AuthContext } from "../helper/AuthContext";

const Add = () => {
  const { name, email } = useContext(AuthContext);

  const addItem = (
    itemName,
    found,
    desc,
    location,
    tags,
    img,
    radius,
  ) => {
    var data = new FormData();
    data.append("name", itemName);
    data.append("desc", desc);
    data.append("found", found);
    data.append("latitude", location[0]);
    data.append("longitude", location[1]);
    data.append("radius", radius);
    data.append("tags", tags);
    data.append("email", email);
    img.forEach((i) => {
      // Append multiple files to request form
      data.append("image", i);
    });

    axios({
      method: "post",
      url: "/items",
      data: data,
      headers: { "Content-Type": "multipart/form-data" },
    });
  };

  return (
    <React.Fragment>
      <h1>Add Item</h1>
      <AddItem addItem={addItem} />
    </React.Fragment>
  );
};
export default Add;
