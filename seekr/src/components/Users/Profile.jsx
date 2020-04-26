import React from "react";
import img from "../../../../uploadedImages/temp.jpg";
import "../../App.css";

export default function Profile() {
  const name = "Andrew";
  const email = "email@email.com";

  return (
    <div className="profile">
      <img src={img} className="profile-pic" />
      <ul style={{paddingLeft: "0pt"}}>
        <div className="contact-info">{name}</div>
        <div className="contact-info">{email}</div>
      </ul>
    </div>
  );
}
