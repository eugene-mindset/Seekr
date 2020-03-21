# Second Iteration Design and Plans

## Objected Oriented Design

### UML Diagram

![UML Diagram](./additional/uml2.jpg)

## Wireframe

![Wireframe](./additional/wireframe2.jpg)

## Iteration Backlog

### User Stories to implement...

* As someone who lost or found something, I want to be able to search for items, so if can see the listings that match by query.
* As someone who has lost something, I want to set a pin on a map of where I think I lost it, so that other users can see it and determine if the item they found might belong to me.

## Tasks

- [X] Add item matching to search bar
- [X] Add test code for search bar
- [X] Add location field for item listings
- [X] Allow user to supply location information when creating a listing
- [X] Deploy on AWS
- [x] Have unit testing
- [x] Set up continous integration with Travis CI
- [X] Switch to object-oriented model

## Retrospective
This iteration, we focused on adding more features for our items and also made some behind-the-scenes changes. We added the ability to select a location for each Item so in future iterations our filtering when searching can be more sophisticated. Behind-the-scenes, we deployed our app onto AWS to make it accessibile to the public, and so none of our computers needed to always host the backend and server. We were able to set up Travis CI to make sure that our tests were able to automatically run. In addition, we changed the structure of our code to better reflect the object-oriented nature of the course. Overall, this iteration was very successful, and we were all able to contribute a lot to our project.


