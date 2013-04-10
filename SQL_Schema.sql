create table Users(
	username varchar(20) not null,
	password varchar(20),
	primary key(username) on cascade delete
)

create table Emails(
	address varchar(30) not null,
	subscribed bool,
	primary key(address) on cascade delete
)

create table has(
	address varchar(30) not null,
	username varchar(20) not null,
	primary key(address, username),
	foreign key(address) references Emails,
	foreign key(username) references Users
)

create table friends_with(
	friend varchar(30),
	friended varchar(30),
	primary key(friend, friended),
	foreign key(fiend) references Users,
	foreign key(friended) references Users
)

create table SecurityQuestions(
	q_id int not null,
	question varchar(30),
	answer varchar(30),
	primary key(q_id),
)

create table secured_with(
	q_id int not null,
	username varchar(20),
	primary key(q_id),
	foreign key(q_id) references SecurityQuestions,
	foreign key(username) references Users
)

create table Events(
	e_id int not null,
	name varchar(20),
	description varchar(100),
	date datetime,
	primary key(e_id)
)

create table favorited(
	username varchar(20),
	e_id int,
	primary key(username, e_id),
	foreign key(username) references Users,
	foreign key(e_id) references Events
)

create table Tags(
	t_id int not null,
	name varhar(20),
	primary key(t_id)
)

create table tagged_with(
	t_id int not null,
	e_id int,
	primary key(t_id, e_id),
	foreign key(t_id) references Tags.
	foreign key(e_id) references Events
)

create table Locations(
	l_id int not null,
	name varchar(30),
	address varchar(30),
	directions varchar(30),
	primary key(l_id)
)

create table located(
	e_id int,
	l_id int,
	primary key(e_id, l_id),
	foreign key(e_id) references Events,
	foreign key(l_id) references Locations
)

create table Preferences(
	p_id int,
	primary key(p_id) on cascade delete
)

create table preferredEvents(
	p_id int,
	e_id int,
	primary key(p_id, e_id),
	foreign key(e_id) references Events,
	foreign key(p_id) references Preferences
)

create table preferredLocations(
	p_id int,
	l_id int,
	primary key(p_id, l_id),
	foreign key(p_id) references Preferences,
	foreign key(l_id) references Locations
)

create table hasPreferences(
	username varchar(20) not null,
	p_id int not null,
	primary key(username, p_id),
	foreign key(username) references Users,
	foreign key(p_id) references Preferences
)
