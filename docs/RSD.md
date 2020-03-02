# Requirement Specification Document

## Problem Statement

> Write a few sentences that describes the problem you are trying to solve. In other words, justify why this software project is needed.

* People lose things all the time, but there is no easy way to check if someone has found your item. If someone finds a lost item, there is no easy way to check who was the one that lost it.

## Potential Clients

> Who are affected by this problem (and would benefit from the proposed solution)? I.e. the potential users of the software you are going to build.

* Anyone in or around the Johns Hopkins community who has lost or found an item.

## Proposed Solution

> Write a few sentences that describes how a software solution will solve the problem described above.

* Develop a website where users can make listings for an item they lost or an item they found. People will be able to enter a description of their item to search and see if anyone has found it.

## Functional Requirements

> List the (functional) requirements that software needs to have in order to solve the problem stated above. It is useful to write the requirements in form of **User Stories** and group them into those that are essential (must have), and those which are non-essential (but nice to have).

### Must have

* As someone who lost something, I want to make a listing for my lost item, so that if someone finds it they can see it.
* As someone who found something, I want to make a listing for an item I found, so if someone has lost the item they can see it.
* As someone who lost or found something, I want to be able to search for items, so if can see the listings that match my query.
* As someone who has lost something, I want to be able to search the listings by the location of where the item was found, so I can have an easier time finding my lost item.
* As someone who has lost something, I want to set a radius on a map of where I think I lost it, so I can be notified if someone finds something in that area.
* As someone who has found something, I want to set a radius on a map of where I found the item, so people can be notified if their item was found in that area.

### Nice to have

* As someone who lost something, I want to see what items are at the JHU lost and found at FastForwardJHU, so I can check if my found item was taken there.
* As someone who lost something, I want to be able to filter items based on designated tags, so I can have an easier time finding an item by its properties or functionality.
* As an admin of JHU Lost and Found at FastForwardJHU, I want to upload specific items that we have found.
* As a user, I want to upload my contact information so someone else knows how to reach me for a lost/found item.
* As a user, I want to log in with my jhed id, so I don’t have to make a new account.
* As a user, I want to search through entries with tags so that it is faster to sort through entries.

## Software Architecture

> Will this be a Web/desktop/mobile (all, or some other kind of) application? Would it conform to the Client-Server software architecture? 

This will be a web app that will work on both desktop and mobile devices. It would conform to the client-server architecture, as users would interact with the webpage to see and create listings, which are handled by the server. Our technology stack will be: Reactjs, Python Flask, MongoDB. The choice for Flask over a Java framework was mostly due to the team's comfort in Python over Java. Also during stack deliberation, it seems as though that Flask had quite a large community over Javalin and so we found it to be a safe bet when it came to debugging issues. MongoDB was chosen due to the fact that we didn't want to be bound by strict schema as with SQL databases. This was just so that we could have more flexibility in how we think about storing data. Also we had planned on potentially leveraging Python data science packages, if needed, when we implement our more advanced features. To keep cohesion in our code base, it made more sense to also choose a python backend framework.
