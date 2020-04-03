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


## Retrospective
This iteration was the first iteration where all of us met online due to the coronavirus. At first, it was a little difficult to work in pairs on tasks that were given to multiple people. However, by using an integration branch, we were able to resolve merge conflicts that occured. We were able to refine our NLP search algorithm, although we think we will continue to make it better throughout the remaining iterations. We also refined our actual item object to be more robust. There is now the feature to add tags and to filter by tags in our search feature. We also added the ability to attach an image. As we add more robustness to the item class, we are thinking about abstracting some of our properties into different classes, such as the map that is included in the item. Overall, this iteration was very productive, and we have a more clear goal with what features we want at the end of Alpha.

