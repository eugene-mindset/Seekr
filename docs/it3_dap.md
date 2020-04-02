# Third Iteration Design and Plans

## Objected Oriented Design

### UML Diagram

![UML Diagram](./additional/uml3.png)

## Wireframe

![Wireframe](./additional/wireframe3.bmp)

## Iteration Backlog

### User Stories to implement

As someone who has lost something, I want to be able to search the listings by the location of where the item was found, so I can have an easier time finding my lost item.
* As someone who lost something, I want to be able to filter items based on designated tags, so I can have an easier time finding an item by its properties or functionality.

## Tasks

### Frontend

#### Home Page

* [X] Eliminate the homepage (Anderson)

#### Add Page

* [X] Allow user to add tags to their listing when they are being created (Andrew)
* [X] Allow user to supply radius when adding a lost item (Jacob)
* [X] Allow user to supply images with their listing (Anderson)

#### Search Page

* [X] Display the timestamp of listings (Anderson)
* [X] Allow user to apply tags to the search bar in order to narrow down listing (Jason & Anderson)
* [X] Allow user to change the order of item listings based on time added, best-matching, etc. (Jason & Anderson)
* [X] List the item as cards (Anderson)
* [X] Display the image belonging to item listing (Anderson)

### Backend

#### Adding Items

* [X] Update backend to get timestamp of when an item was created (Shaurya & Andrew)
* [X] Update backend to get images when a user listing is added (Anderson)
* [X] Update backend to get radius when a user listing is added (Shaurya & Andrew)
* [X] Update backend to get tags when a user listing is added (Shaurya & Andrew)

#### Returning Item Listings

* [X] Allow sorting based on time or best match (Shaurya)
* [X] Improve item listing matching algorithm to match on similar words, not exact (Eugene, Jason and Andrew)
* [X] Add filtering functionality to narrow results down to only those with the desired tags or qualifications (Andrew)
