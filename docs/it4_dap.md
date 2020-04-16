# Fourth Iteration Design and Plans

## Objected Oriented Design

### UML Diagram

![UML Diagram](./additional/uml4.png)

## Wireframe

![Wireframe](./additional/wireframe3.bmp)

## Iteration Backlog

### User Stories to implement

* As someone who has lost something, I want to be able to search the listings by the location of where the item was found, so I can have an easier time finding my lost item.
* As a user, I want to upload my contact information so someone else knows how to reach me for a lost/found item.
* As someone who has lost something, I want to be notified if someone finds an item similar to mine so I don't have to constantly check the website.

## Tasks


* [X] Allow searching based on proximity to a specified location frontend and backend (Jacob)
* [X] Improve search algorithm word matching (Eugene and Jason)
* [X] Allow user to input their contact information when adding an item frontend and backend (Jacob)
* [X] Make adding an image optional instead of required (Jason)
* [X] Notify a user by sending them an email if someone posts a found item similar to their lost item (and vice versa) based on matching the item images and location (Shaurya and Andrew)
* [X] Create a User class and Location class in the backend (Anderson)
* [X] Modify the DAO to properly serialize and deserialize the new Item object structure from the database (Anderson)
* [X] Make database store tags as enums (Eugene)
* [X] Implement algorithm to match similar item images, give a matching score (Anderson)
* [X] Make frontend store tags as enums (Eugene)
* [X] Display the tags an item has on its listing (Andrew)
* [X] Display contact information of a user on the item listing that they posted (Jacob)
* [X] Clear the search when not searching (Andrew)
* [X] Figure out how to deploy better (Jason)
