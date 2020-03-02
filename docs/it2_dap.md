# First Iteration Design and Plans

## Objected Oriented Design

### UML Diagram
![UML Diagram](./additional/)

## Wireframe
![Wireframe](./additional/)


## Iteration Backlog

### User Stories to implement...
* As someone who lost or found something, I want to be able to search for items, so if can see the listings that match by query.
* As someone who has lost something, I want to set a radius on a map of where I think I lost it, so I can be notified if someone finds something in that area.
* As someone who lost something, I want to be able to filter items based on designated tags, so I can have an easier time finding an item by its properties or functionality.

## Tasks
- [ ] Add item matching to search bar
- [ ] Add test code for search bar
- [ ] Add location field for item listings
- [ ] Allow user to supply location information when creating a listing
- [ ] When displaying listings, show the location of where the item was found on a map
- [ ] Allow users to add tags to items to help filter items out
- [ ] Deploy on Heroku
- [ ] Have tests for new and old code

## Retrospective
We were able to accomplish all of the tasks we listed. From the first iteration, we wanted to implement the basic CRUD functionalities for our lost-and-found app. Despite choosing a stack that was not covered in class (React, Flask, MongoDB), the team was able to get started relatively quickly. The only difficulty we had this iteration was setting up the environment. Since everyone was using a different laptop with different software, we needed to set up a virtual environment for our program so everything could work for everyone. We realized that the steps to set up and run the virtual environment are different between operating systems, so it took a while to make the changes. After setting everything up, we used various tutorials to set up the React frontend and Flask backend. For the next iteration, we will focus on implementing features that would make our program more than just a regular CRUD app, including adding Google Maps API integration, better searching, and deploying on Heroku. We also will reformat some of our code, so that it will be easier to work with in the future.
