# [Library Admin](http://city-public-library.eba-9hgqkiku.us-west-2.elasticbeanstalk.com "City Public Library Admin Site")
Link to site: [http://city-public-library.eba-9hgqkiku.us-west-2.elasticbeanstalk.com](http://city-public-library.eba-9hgqkiku.us-west-2.elasticbeanstalk.com "City Public Library Admin Site")

## Table of Contents
- [Overview](#overview "Overview")
- [Usage](#usage "Usage")
  - [Visit Library Admin](#visit "Library Admin")
  - [Members](#members "Members")
  - [Libraries](#libraries "Libraries")
  - [Books and Authors](#books "Books and Authors")
  - [Resources](#resources "Resources")
  - [Rentals and Rental Items](#rentals "Rentals and Rental Items")
- [Database Design](#database "Database Design")
  - [Diagrams](#diagrams "Diagrams")
  - [Outline](#outline "Outline")

## Overview <a name="overview"></a>
This project is a mock library administrative web app for the imaginary City Public Library network. The library admin site allows library workers to view, edit, add, and delete members, library branches, books, rentals, and resources (stocks of books at a particular branch). In a real production scenario, the web app would include user authentication; however, that was foregone in this mockup to make it more easily explorable. The application is written using Python, HTML/CSS, Django, and Bootstrap. It is deployed through Amazon Web Service's Elastic Beanstalk with a MySQL database.

## Usage <a name="usage"></a>

### Visit Issue Tracker <a name="visit"></a>
Visit Library Admin's home page at the public URL: [http://city-public-library.eba-9hgqkiku.us-west-2.elasticbeanstalk.com](http://city-public-library.eba-9hgqkiku.us-west-2.elasticbeanstalk.com "City Public Library Admin Site")

![Home page](https://github.com/realKP/library-admin/assets/76978772/2d0c94d5-06fb-4a40-bef3-5795e17b96bf)

### Members <a name="members"></a>
In the Members tab, members can be added or deleted by clicking either of the respective buttons on the page. To update a particular member's personal information or view their rental history, click the _View_ button on that member's row in the table.

![Members page](https://github.com/realKP/library-admin/assets/76978772/0b892a99-88cc-4593-9537-523b2d46f6a8)

![Add new member modal](https://github.com/realKP/library-admin/assets/76978772/6d664805-12e8-4a2f-a1e0-58fbfbacd6df)

![Delete member modal](https://github.com/realKP/library-admin/assets/76978772/4f80e590-2291-4193-a16c-f8d6fc2b7aa5)

![Specific member view page](https://github.com/realKP/library-admin/assets/76978772/d689b8da-d9f2-45db-aa0f-ee7cd5e525f2)

The details and items in a particular rental (rental items) can be viewed by clicking _View_ on a specific rental in a member's rental history. More on this in the [Rentals and Rental Items section](#rentals "Rentals and Rental Items").

### Libraries <a name="libraries"></a>
To view a particular library's information such as the resources available at that library or the rentals from that library, click the _View_ button on that library's row in the table. On a specific library's page, new resources can be added or new rentals created by clicking the respective button.

![Libraries page](https://github.com/realKP/library-admin/assets/76978772/bb2229bf-6156-4cfd-b0cc-2c6e7f97a2ea)
![Specific library branch page](https://github.com/realKP/library-admin/assets/76978772/d64c3cde-9a74-44f2-89d9-bd6ce46977da)
![Add new resource modal](https://github.com/realKP/library-admin/assets/76978772/8eb6e8c4-7c6c-40ab-9bbd-127186491488)
![Create new rental modal](https://github.com/realKP/library-admin/assets/76978772/daec2c84-a002-479e-b312-3b5f22c40dd6)

The details and items in a particular rental (rental items) can be viewed by clicking _View_ on a specific rental in the rentals table. More on this in the [Rentals and Rental Items section](#rentals "Rentals and Rental Items"). To edit a resource, click _Edit_ on a specific resource in the resources table. More on this in the [Resources section](#resources "Resources").

### Books and Authors <a name="books"></a>
In the Books tab, books can be added by clicking the _Add New Book_ button. This is also where new authors are added and connected to their books. To view which library branches have a particular book, click the _Availability_ button on a specific book in the books table. Clicking _View Library_ in the modal will redirect to that branch's specific page.

![Books page](https://github.com/realKP/library-admin/assets/76978772/6a034927-7d97-4d78-8e5b-4fee36c3b271)
![Add new book modal](https://github.com/realKP/library-admin/assets/76978772/c218b061-b367-498e-88f7-fb7d294eaf0a)
![Resource availability modal](https://github.com/realKP/library-admin/assets/76978772/3778d8f3-0188-4b95-9ad7-6fa3ae025b9b)

### Resources <a name="resources"></a>
In the Resources tab, resources can be added by clicking the _Add New Resource_ button.

![Resources page](https://github.com/realKP/library-admin/assets/76978772/06d95546-434e-45ab-a046-b72844cb7a7f)
![Add new resource modal](https://github.com/realKP/library-admin/assets/76978772/b2003693-a123-4058-9c69-50792e32cb6f)

To edit a particular resource's quantity available, click the _Edit_ button on that resources's row in the table. This page can also be found through the page of the specific library branch at which the resource is located, as mentioned in the [Libraries section](#libraries "Libraries") previously.

![Edit specific resource page](https://github.com/realKP/library-admin/assets/76978772/a6e996c2-ecca-4433-9d5b-1301a6602cad)


### Rentals and Rental Items <a name="rentals"></a>
There are two ways to access rentals and the rental items included in those rentals. The first is through a particular member's page as described in the [Members section](#members "Members"). The second is through a particular library branch's page as described in the [Libraries section](#libraries "Libraries"). Both methods are depicted again in the following two images:

![Specific member page](https://github.com/realKP/library-admin/assets/76978772/808361fb-d00c-425e-8a7b-9a7490c5a286)
![Specific library page](https://github.com/realKP/library-admin/assets/76978772/83a59ef9-e268-4e0e-8b24-a07db6ddd9c3)

From either of the two aformentioned pages, clicking _Edit_ on a rental in the rentals table will direct you to a page similar to the first one shown below. From this page, a particular rental item in the rental can be edited by clicking the _Edit_ button. From this page (as shown in the second image), the return date and status can be updated.

![Specific rental page](https://github.com/realKP/library-admin/assets/76978772/a21bd491-aba5-45f7-9290-2bad3a291411)
![Specific rental item page](https://github.com/realKP/library-admin/assets/76978772/100fb59e-2bb6-48a3-90e8-03b8735c60a7)


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

- Books_Authors: an intersection table between Books and Authors.
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

