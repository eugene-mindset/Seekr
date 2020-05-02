# Fifth Iteration Design and Plans

## Objected Oriented Design

### UML Diagram

![UML Diagram](./additional/uml5.png)

## Wireframe

![Wireframe](./additional/wireframe3.bmp)

## Iteration Backlog

### User Stories to implement

* As a user, I want to log in with my Facebook or Google account, so I don’t have to make a new account.

## Tasks

### Add

* [X] Set boundary for radius (no negative) should be front end (Anderson)
* [X] Clean up add item page (Anderson)
  * [X] Make map look smaller? (Andrew)
  * [X] Make it easy to tell what inputs of the form are (radius, images) (Anderson)
* [X] Limit so people can only upload a 12 mb picture (Anderson)
* [X] Change the database so that items save images as binaries rather than images locally (Anderson)
* [X] Allow the user to add multiple images when creating a listing (Anderson)

### Search

* [X] Move the search bar to side (Andrew)
* [X] Displaying search boxes (clicking search box should display bigger box and generating mini map) (Jacob)
* [X] Make mini-map for item listing cards be attached to the respective cards (Jacob)
* [X] Prevent the client from sending multiple search requests to the backend until it gets the information from the first request (Jacob)
* [X] Have a loading symbol appear on the search page when the user is searching for an item but has yet to get results back (Jacob)
* [x] Have gensim download file if it is not on directory, otherwise use the one in there (Eugene)

### User Accounts

* [X] Add user authentication (Shaurya, Andrew)
* [X] Provide the option to opt out of email notifications for users (Shaurya, Andrew)
* [X] Users can only delete their own post (Shaurya, Andrew)
* [X] Add the button for authentication (Shaurya, Andrew)

### General

* [X] Improve design of the website
  * [X] Improve navbar (Jason)
  * [X] Get rid of ugly fonts and colors (Collaboration)
  * [X] Footer for page, get rid of the about page (Jason)
* [X] Document existing code (Everyone)
* [X] Delete any unused code (Eugene)
* [X] Deploy in production mode (Jason)
* [X] Remove all python wildcard imports and replace them with exact imports (Eugene)
* [X] Add more test cases (Eugene, Anderson, Jacob, Shaurya)
* [X] Update dependencies (Jason)

### Retrospective

In this iteration we put the final touches on our app. We were able to implement the original vision we had for our application in this iteration. One of the biggest changes we made was to the frontend, in order to make the user experience as good as possible. We feel we have delievered on all our original goals. The biggest challenge was doing this during this difficult time. We also had difficulty of doing a full deployment with SSL, a domain name, and nginx on AWS. It turned out well all things considered, and we believe we have a fully functional application and learned a tremendous amount about various web technologies and development practices along the way.
