import React, { useState } from "react";
import "../../App.css";
import { useContext } from "react";
import { AuthContext } from "../helper/AuthContext";
import Checkbox from "../item/Checkbox";
import axios from "axios";
import { Image, Jumbotron, Button} from "react-bootstrap";


export default function Profile() {
  const { name, email, profilePic } = useContext(AuthContext);
  const label = " Email me if someone posts an item that could be mine";

  const [isOptIn, setOptIn] = useState(false);

  const getState = (isChecked) => {
    // setOptIn(isChecked);
    // console.log(!isChecked);
    setOptIn(!isChecked);
    console.log(isOptIn);
  };

  const toggleCheckbox = () => {
    // toggleCheckbox is called whenever there is a change in the state of the Checkbox
    // this is where u would call the API to turn on/off opt in
    var data = new FormData();
    data.append("username", name);
    data.append("email", email);
    data.append("optIn", isOptIn);

    axios({
      method: "put",
      url: "/api/userinfo",
      data: data,
      headers: { "Content-Type": "multipart/form-data" },
    });
  };

  return (
    <div className="profile">
      <Jumbotron>
        <Image src={profilePic} roundedCircle style={{  height: '100x', width: '100px'}} />
        <h1>Hi, {name}!</h1>
        <ul className="profile-info" style={{ paddingLeft: "0pt" }}>
          <br></br>
          <p><b><i>Information About You</i></b></p>
          <p><b>Name:</b> {name}</p>
          <p><b>Contact Email:</b> {email}</p>
          <br></br>
          <div style={{marginLeft: "10px"}}>
            <Checkbox
              label={label}
              // flagValue={label}
              toggleCheckbox={toggleCheckbox}
              key={label}
              getState={getState}
            />
          </div>
        </ul>
        <p>
          {/* <Button variant="primary">Learn more</Button> */}
        </p>
      </Jumbotron>
    </div>
  );
}
