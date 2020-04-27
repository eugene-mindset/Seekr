import React from "react";
import img from "../../../../uploadedImages/temp.jpg";
import "../../App.css";
import { useContext } from "react";
import { AuthContext } from "../helper/AuthContext";
import Checkbox from "../item/Checkbox";

export default function Profile() {
  const { name, email, profilePic } = useContext(AuthContext);
  const label = " Email me if someone posts an item that could be mine";

  const toggleCheckbox = () => {
    // toggleCheckbox is called whenever there is a change in the state of the Checkbox
    // this is where u would call the API to turn on/off opt in
    return console.log("hello");
  };

  return (
    <div className="profile">
      {/* TODO: img is a temporary picture */}
      <img src={img} className="profile-pic" />
      <div>
        <ul className="profile-info" style={{ paddingLeft: "0pt" }}>
          <div className="contact-name">{name}</div>
          <div className="contact-email">{email}</div>
          <br></br>
          <div style={{marginLeft: "10px"}}>
            <Checkbox
              label={label}
              // flagValue={label}
              toggleCheckbox={toggleCheckbox}
              key={label}
            />
          </div>
        </ul>
      </div>
    </div>
  );
}
