# Fourth Iteration Design and Plans

## Objected Oriented Design

### UML Diagram

![UML Diagram](./additional/uml4.png)

## Wireframe

![Wireframe](./additional/wireframe4.bmp)

## Iteration Backlog

### User Stories to implement

* As someone who has lost something, I want to be able to search the listings by the location of where the item was found, so I can have an easier time finding my lost item.
* As a user, I want to upload my contact information so someone else knows how to reach me for a lost/found item.
* As someone who has lost something, I want to be notified if someone finds an item similar to mine so I don't have to constantly check the website.

## Tasks

#### Search

* [ ] Allow searching based on proximity to a specified location
* [ ] Improve search algorithm word matching

#### Adding

* [ ] Allow user to input their contact information when adding an item
* [ ] Make adding an image optional instead of required

#### Notifications

* [ ] Notify a user by sending them and email if someone posts a found item similar to their lost item (and vice versa) based on matching the item images and location

#### Database

* [ ] Create a User class and Location class in the backend
* [ ] Modify the DAO to properly serialize and deserialize the new Item object structure from the database
* [ ] Handle adding the new parameters for an item into the database

#### Image Recognition

* [ ] Implement algorithm to match similar item images

#### Frontend

* [ ] Display the tags an item has on its listing
* [ ] Display contact information of a user on the item listing that they posted
