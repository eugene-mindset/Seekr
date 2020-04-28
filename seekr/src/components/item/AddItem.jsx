import React, { Component } from 'react'
import PropTypes from 'prop-types';
import GoogleMap from '../pages/GoogleMap';
import Checkbox from "./Checkbox";
import ItemTags from "../helper/ItemTags";
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button'

export class AddItem extends Component {

  state = {
    name: '',
    desc: '',
    found: false,
    location: [39.3299, -76.6205],
    radius: 25,
    tags: 0,
    img: [],
    username: "",
    email: "",
    phone: ""
  }
  
  toggleCheckbox = val => {
    if ((this.state.tags & val) === val) {
      this.setState(prevstate => ({ tags: prevstate.tags & ~(val)}))
    } else {
      this.setState(prevstate => ({ tags: prevstate.tags | val}))
    }
  };

  createCheckbox = tag => (
    <Checkbox
      label={tag.label}
      flagValue={tag.value}
      toggleCheckbox={this.toggleCheckbox}
      key={tag.label}
    />
  );

  createCheckboxes = () => ItemTags.getMapping().map(this.createCheckbox);

  callbackFunction = (coordinates) => {
    this.setState({location: coordinates})
  }

  clearForm = () => {
    this.setState({
      name: '',
      found: false,
      desc: '',
      location: [39.3299, -76.6205],
      img: [],
      radius: 0,
      username: "",
      email: "",
      phone: ""
    });

    document.getElementById("imagesUpload").value = "";

    let radios = document.getElementsByName('lostfoundradio');
    for (let i = 0; i < radios.length; i++) {
      radios[i].checked = false;
    }

    var boxes = document.getElementsByClassName('box');
    for (let box of boxes) {
      if (box.checked) {
        box.click();
      }
    }
  }

  onClick = (e) => {
    this.setState({found: true});
  }

  onSubmit = (e) => {

    e.preventDefault();

    this.props.submitForm(this.state.name, this.state.found, this.state.desc, this.state.location, this.state.tags,
      this.state.img, this.state.radius, this.state.username, this.state.email, this.state.phone);

    this.clearForm();
  }

  onChange = (e) => this.setState({ [e.target.name]: e.target.value });

  validateFiles = (uploadedFiles) => {
    // Check to make sure images are below 12 Mib, and that they are only png or jpg
    let totalSize = 0;

    uploadedFiles.forEach(imgFile => {
      if (imgFile.type !== 'image/png' && imgFile.type !== 'image/jpeg') {
        alert('Only .png and .jpeg files are allowed.');
        return false;
      }
      totalSize += imgFile.size
    });

    totalSize = (totalSize / 1024) / 1024 // Convert from bytes to MiB
    if (totalSize >= 12) {
      let alertString = `Total image upload limit is 12 MB. You have uploaded ${totalSize} MB of images.`
      alert(alertString);
      return false;
    }
    return true;
  }

  fileSelectedHandler = (e) => {
    this.setState({
      img: []
    });

    var uploadedFiles = []
    for (let i = 0; i < e.target.files.length; i++) {
      uploadedFiles.push(e.target.files[i])
    }

    let filesOK = this.validateFiles(uploadedFiles);

    if (!filesOK) {
      document.getElementById("imagesUpload").value = "";
      return false;
    }

    this.setState({
      img: uploadedFiles
    });
  }

  lostFoundClick = (e) => {
    this.setState({ found: e.target.value === 'true' })
    // If item is a found item, user shouldn't have to select a radius
    if (e.target.value === 'true') {
      document.getElementById('formRadiusGroup').style.display = 'none';
    } else {
      document.getElementById('formRadiusGroup').style.display = 'block';
    }
  }

  radiusOnChange = (e) => {
    let selected = e.target.value;
    let distance = selected.substring(0, selected.length - 5);
    this.setState({ radius: parseInt(distance, 10)});
  }

  render() {
    return (
      // flexbox
      <div style={{border: '3px solid', borderRadius: '10px', margin: 'auto', width: '70%', minWidth: '600px', padding: '20px', backgroundColor: 'white'}}>
        <Form onSubmit={this.onSubmit} style={{ textAlign : 'left'}}>
          <Form.Group >
            <Form.Label>Did you lose or find this item?</Form.Label>
            <Form.Check
              type='radio'
              label='I lost it'
              name='lostfoundradio'
              value='false'
              onClick={this.lostFoundClick}
              required
            />
            <Form.Check
              type='radio'
              label='I found it'
              name='lostfoundradio'
              value='true'
              onClick={this.lostFoundClick}
            />
          </Form.Group>

          <Form.Group controlId='formItemName'>
            <Form.Label>Item name</Form.Label>
            <Form.Control
              type='text'
              name='name'
              placeholder='Enter item name...'
              value={this.state.name}
              onChange={this.onChange}
              required
            />
            <Form.Text className='text-muted'>
              Enter the name of the item.
            </Form.Text>
          </Form.Group>

          <Form.Group controlId='formDescArea'>
            <Form.Label>Item description</Form.Label>
            <Form.Control
              name='desc'
              as='textarea'
              rows='3'
              placeholder='Enter item description...'
              value={this.state.desc}
              onChange={this.onChange}
            />
            <Form.Text className='text-muted'>
              Enter a description of the item.
            </Form.Text>
            <Form.Text className='text-muted'>
              Note: You may not want to put all the details of an item. If someone contacts you
              regarding the item, ask them to describe some of the details of it first before giving
              it to them.
            </Form.Text>
          </Form.Group>

          <Form.Group>
            <Form.Label>What kind of item is it?</Form.Label>
            <div style={{ display: "flex", width:"50%", justifyContent: 'space-between' }}>{this.createCheckboxes()}</div>
          </Form.Group>

          <Form.Group>
            <Form.Label>Where did you lose/find the item?</Form.Label>
            <div style={{marginBottom: '260px', position: 'relative', zIndex: '0'}}>
              <GoogleMap parentCallback={this.callbackFunction} clickable={true}/>
            </div>
            <Form.Text className='text-muted'>
              Click on the map to place a marker.
            </Form.Text>
          </Form.Group>

          <Form.Group id='formRadiusGroup' controlId='formRadius'>
            <Form.Label>
              Within what distance do you think you lost the item from this location?
            </Form.Label>
            <Form.Control as='select' onChange={this.radiusOnChange}>
              <option>25 feet</option>
              <option>50 feet</option>
              <option>75 feet</option>
              <option>100 feet</option>
            </Form.Control>
          </Form.Group>

          <Form.Group controlId='formImages'>
            <Form.Label>Upload any images of the item that you may have.</Form.Label>
            <input
              type="file"
              id="imagesUpload"
              multiple
              accept="image/png, image/jpeg"
              onChange={this.fileSelectedHandler}
              style={{ display: 'block'}}
            />
          </Form.Group>

          <Form.Group controlId='formName'>
            <Form.Label>
              Enter your contact information so people can contact you about the item.
            </Form.Label>
            <Form.Control
              type="text"
              name="username"
              placeholder="Enter your name..."
              value={this.state.username}
              onChange={this.onChange}
            />
          </Form.Group>

          <Form.Group controlId='formEmail'>
            <Form.Control
              type="email"
              name="email"
              placeholder="Enter your email..."
              value={this.state.email}
              onChange={this.onChange}
            />
          </Form.Group>

          <Form.Group controlId='formPhone'>
            <Form.Control
              type="tel"
              name="phone"
              placeholder="Enter your phone number..."
              value={this.state.phone}
              onChange={this.onChange}
            />
          </Form.Group>

          <Button variant="primary" type="submit">
            Submit
          </Button>
        </Form>
      </div>
    )
  }
}

AddItem.propTypes = {
  submitForm: PropTypes.func.isRequired
}

export default AddItem;
