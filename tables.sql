create table Users(
	username varchar2(30) primary key,
	password varchar2(30)
);

create table Emails(
	address varchar2(30) primary key,
	subscribed number(1);
);

create table has(
	address varchar2(30),
	username varchar2(20),
	primary key(address, username),
	foreign key(address) references Emails,
	foreign key(username) references Users on delete cascade
);

create table friends_with(
	friend varchar2(30),
	friended varchar2(30),
	primary key(friend, friended),
	foreign key(friend) references Users,
	foreign key(friended) references Users
);

create table SecurityQuestions(
	q_id number(1) primary key,
	question varchar2(30),
	answer varchar2(30),
	username varchar2(3) not null,
	foreign key(username) references Users on delete cascade
);

create table Events(
	e_id integer primary key,
	name varchar2(30),
	description varchar2(100),
	dateof date
);

create table favorited(
	username varchar2(20),
	e_id integer,
	primary key(username, e_id),
	foreign key(username) references Users,
	foreign key(e_id) references Events
);

create table Tags(
	t_id integer,
	name varchar(20),
	primary key(t_id)
);

create table tagged_with(
	t_id integer,
	e_id integer,
	primary key(t_id, e_id),
	foreign key(t_id) references Tags.
	foreign key(e_id) references Events
);

create table Locations(
	l_id integer,
	name varchar2(30),
	address varchar2(30),
	directions varchar2(30),
	primary key(l_id)
);

create table located(
	e_id integer,
	l_id integer,
	primary key(e_id, l_id),
	foreign key(e_id) references Events,
	foreign key(l_id) references Locations
);

create table Preferences(
	p_id integer,
	primary key(p_id)
);

create table preferredEvents(
	p_id integer,
	e_id integer,
	primary key(p_id, e_id),
	foreign key(e_id) references Events,
	foreign key(p_id) references Preferences on delete cascade
);

create table preferredLocations(
	p_id integer,
	l_id integer,
	primary key(p_id, l_id),
	foreign key(p_id) references Preferences on delete cascade,
	foreign key(l_id) references Locations
);

create table hasPreferences(
	username varchar2(20),
	p_id integer,
	primary key(username, p_id),
	foreign key(username) references Users,
	foreign key(p_id) references Preferences on delete cascade
);