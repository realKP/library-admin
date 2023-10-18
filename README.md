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
This project is a mock library administrative web app for the imaginary City Public Library network. The library admin site allows library workers to view, edit, add, and delete members, library branches, books, rentals, and resources (stocks of books at a particular branch). In a real production scenario, the web app would include user authentication; however, that was foregone in this mockup to make it more easily explorable. The application is written using Python, Django, and Bootstrap. It is deployed through Amazon Web Service's Elastic Beanstalk with a MySQL database.

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


![Database schema](https://github.com/realKP/library-admin/assets/76978772/dc9edcf2-10ba-4a80-8757-ae297664ff25)


### Outline <a name="outline"></a>
_Note: since most attributes are not nullable, nullable is used where attributes can be NULL_

- Members: records the details of members that belong to the library network.
  - member_ID: INT, auto increment, unique, PK
  - member_first_name: VARCHAR
  - member_last_name: VARCHAR
  - member_phone: VARCHAR
  - member_email: VARCHAR
  - Relationships:
    - A Rental request can have only one Member associated with it, but a Member can have zero or more Rentals.

- Rentals: records the details of the rental requests from members.
  - rental_ID: INT, auto increment, unique, PK
  - member_ID: INT, FK
  - library_ID: INT, FK
  - rental_date: DATE
  - Relationships:
    - a 1:M relationship between Rentals and Rental_Items with rental_ID as FK in Rental_Items
    - see Libraries

- Rental_Items: records the information about a specific line item for a resource in a
rental request. Each member can only rent a single instance of a resource per rental
request.
  - rental_ID: INT, FK, composite PK
  - resource_ID: INT, FK, composite PK
  - queue_num: INT
  - rental_item_status: VARCHAR
  - return_date: DATE nullable
  - Relationships:
  - Is the relation table for the M:M between Rentals and Resources
  - see Rentals
  - see Resources

- Resources: records the stock of a book at a particular library in the network.
  - resource_ID: INT, auto increment, unique, PK
  - isbn: VARCHAR, FK
  - library_ID: INT, FK
  - quantity_available: INT
  - quantity_checked_out: INT
  - Relationship: a 1:M relationship between Resources and Rental_Items with
  resource_ID as FK in Rental_Items
  - see Libraries
  - see Books

- Books: records the title of a book that may or may not be a resource in the network.
  - isbn: VARCHAR, unique, PK
  - book_title: VARCHAR
  - Relationships: a 1:M relationship between Books and Resources with isbn as FK
  in Resources
  - See Books_Authors

- Authors: records the different authors of books.
  - author_ID: INT, auto increment, unique, PK
  - author_name: VARCHAR
  - Relationships: see Books_Authors

-Books_Authors: an intersection table between Books and Authors.
  - author_ID: INT, FK, composite PK
  - isbn: VARCHAR, FK, composite PK
  - Relationships: 1:M relationships with each Books and Authors with their PKs
  comprising the composite PK of the intersection table.
  - Is the relationship table for the M:M between Books and Authors

- Libraries: records the details of libraries in the network.
  - library_ID: INT, auto increment, unique, PK
  - library_name: VARCHAR
  - library_address: VARCHAR
  - Relationships: a 1:M relationship between Libraries and Rentals with library_ID as
  FK in Rentals
  - Relationships: a 1:M relationship between Libraries and Resources with library_ID
  as FK in Rentals

