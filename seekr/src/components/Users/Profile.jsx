import React from "react";
import img from "../../../../uploadedImages/temp.jpg";
import "../../App.css";
import { useContext } from "react";
import { AuthContext } from "../helper/AuthContext";

export default function Profile() {
  const { name, email, profilePic } = useContext(AuthContext);

  return (
    <div className="profile">
      <img src={img} className="profile-pic" />
      <ul style={{ paddingLeft: "0pt" }}>
        <div className="contact-info">{name}</div>
        <div className="contact-info">{email}</div>
      </ul>
    </div>
  );
}
