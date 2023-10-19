# [Library Admin](http://city-public-library.eba-9hgqkiku.us-west-2.elasticbeanstalk.com "City Public Library Admin Site")
Link to site: [http://city-public-library.eba-9hgqkiku.us-west-2.elasticbeanstalk.com](http://city-public-library.eba-9hgqkiku.us-west-2.elasticbeanstalk.com "City Public Library Admin Site")

## Table of Contents
- [Overview](#overview "Overview")
- [Usage](#usage "Usage")
  - [Visit Library Admin](#visit "Library Admin")
- [Database Design](#database "Database Design")
  - [Diagrams](#diagrams "Diagrams")
  - [Outline](#outline "Outline")

## Overview <a name="overview"></a>
This project is a mock library administrative web app for the imaginary City Public Library network. The library admin site allows library workers to view, edit, add, and delete members, library branches, books, rentals, and resources (stocks of books at a particular branch). In a real production scenario, the web app would include user authentication; however, that was foregone in this mockup to make it more easily explorable. The application is written using Python, HTML/CSS, Django, and Bootstrap. It is deployed through Amazon Web Service's Elastic Beanstalk with a MySQL database.

## Usage <a name="usage"></a>

### Visit Issue Tracker <a name="visit"></a>
Visit Library Admin's home page at the public URL: [http://city-public-library.eba-9hgqkiku.us-west-2.elasticbeanstalk.com](http://city-public-library.eba-9hgqkiku.us-west-2.elasticbeanstalk.com "City Public Library Admin Site")

![image](https://github.com/realKP/library-admin/assets/76978772/a29f1e27-4d7b-4dd0-9e38-5fd24cfa3c66)


## Database Design <a name="database"></a>
To provide more detail on how the data in this app relate to each other, I have provided the entity relationship diagram (ERD), schema, and outline used to create the database.

### Diagrams <a name="diagrams"></a>
#### Entity Relationship
For a thorough explanation of the notation used in the ERD below, feel free to read [this article](https://www.freecodecamp.org/news/crows-foot-notation-relationship-symbols-and-how-to-read-diagrams/ "Crow's Foot Notation").


![Entity relationship diagram](https://github.com/realKP/library-admin/assets/76978772/862ec2cb-d8dd-45dd-bad5-05eab60a2eab)

#### Schema
The schema below illustrates the primary and foreign key relationships between the various entities. The underlined attributes are the primary key for that entity.


![image](https://github.com/realKP/library-admin/assets/76978772/fa7ae6b8-fab2-4651-beef-4548766d682e)


### Outline <a name="outline"></a>
_Note: since most attributes are not nullable, nullable is used where attributes can be NULL_

- Members: records the details of members that belong to the library network.
  - member_ID: INT, auto increment, unique, PK
  - member_first_name: VARCHAR
  - member_last_name: VARCHAR
  - member_phone: VARCHAR
  - member_email: VARCHAR
  - Relationships:
    - A Rental can have only one Member associated with it, but a Member can have zero or more Rentals.

- Rentals: records the details of the rental requests from members.
  - rental_ID: INT, auto increment, unique, PK
  - member_ID: INT, FK
  - library_ID: INT, FK
  - rental_date: DATE
  - rental_status: VARCHAR
  - Relationships:
    - A Library can have zero or more Rentals, but a Rental can have only one Library associated with it.
    - A Rental Item can only be associated with one Rental, but a Rental can have one or more Rental Items.
    - _See Members_

- Rental_Items: records the information about a specific line item for a resource in a rental request.
  - rental_item_ID: VARCHAR, unique, PK
  - rental_ID: INT, FK
  - resource_ID: INT, FK
  - queue_num: INT
  - rental_item_status: VARCHAR
  - return_date: DATE nullable
  - Relationships:
    - A Resource can have zero or more Rental Items associated with it, but a Rental Item can only refer to one Resource.
    - _See Rentals_

- Resources: records the stock of a book at a particular library branch in the network.
  - resource_ID: INT, auto increment, unique, PK
  - isbn: VARCHAR, FK
  - library_ID: INT, FK
  - quantity_available: INT
  - quantity_checked_out: INT
  - queue_num: INT
  - Relationship: 
    - A Library can have one or more Resources, but a Resource can only belong to one Library.
    - A Book can be associated with zero or more Resources, but a Resource can refer to only one Book.
    - _See Rental_Items_

- Books: records the title of a book that may or may not be a resource in the network.
  - isbn: VARCHAR, unique, PK
  - book_title: VARCHAR
  - Relationships:
    - A Books_Author can belong to only one Book, but a Book can have one or more Books_Authors.
    - _See Resources_

- Authors: records the different authors of books.
  - author_ID: INT, auto increment, unique, PK
  - author_name: VARCHAR
  - Relationships:
    - A Books_Author can refer to only one Author, but an Author can have zero or more Books_Authors relations.

-Books_Authors: an intersection table between Books and Authors.
  - author_ID: INT, FK, composite PK
  - isbn: VARCHAR, FK, composite PK
  - Relationships:
    - _See Books_
    - _See Authors_

- Libraries: records the details of library branches in the network.
  - library_ID: INT, auto increment, unique, PK
  - library_name: VARCHAR
  - library_address: VARCHAR
  - Relationships:
    - _See Rentals_
    - _See Resources_

