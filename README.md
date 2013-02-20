CUNom
=====

(Databases Project with Sophie)

Description: CUNom is a disruptive web application to help students survive the perils of college life. Too often college students starve due to the cost of quality food around campus, when in fact free food events happen for nearly every meal of the day everyday. CUNom presents aggregated information about free food events on campus through an easy to use search interface. Users can go to the website and search for free food by keywords, tags, locations, and date, as well as create an account to receive email notifications about upcoming free food. Here the events info will be taken from the Events Table (with attributes for date, discription, name). User searches will in fact query our database for events and user accounts will also be created within our database. We will also have a Preferences table so that users can store what locations, and events they prefer (for future reference). We hope to build the implement the front-end option and create the website using the light-weight Python framework Flask built on top of a MySQL database.

Database Schema: We will have tables for Users, Emails, SecurityQuestions, Events, Tags, Locations, and Preferences. For Users we will have a primary key constraint with username. If we look at the has table that we use to connect Users with Emails, we see a foreign key constraint with Users, such that we reject any has tuple with a non-existent u\_id. This foreign key constraint holds for SecurityQuestions as well. Furthermore, Events & Tags are related through a tagged_with table that also shares a foreign key constraint in that ever Tag in the Tags table must appear in the relation table tagged_with (total participation). Please refer to our E/R diagram and SQL schemas for more info.

Data Source: We will scrape the popular Columbia blog BWOG for most of our information on free food events. Information on users and their preferences will be populated through user input either during signup or through a preferences panel on the website.

