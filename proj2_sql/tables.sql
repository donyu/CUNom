create type image as object (
	idno integer,
	alt_text varchar2(30),
	src varchar2(30),
	map member function 

) not final;

create type profile_image under image (
	thumbnail_src varchar2(30),
	overriding member function show_alt return varchar2
) not final;

create table Users(
	username varchar2(30) primary key,
	password varchar2(30) check (length(password) > 3),
	prof_pic profile_image
);

create table Emails(
	address varchar2(30) primary key,
	subscribed number(1) check (subscribed = 0 or subscribed = 1)
);

create table has(
	username varchar2(30),
	address varchar2(30),
	primary key(username, address),
	foreign key(address) references Emails,
	foreign key(username) references Users on delete cascade
);

create table friends_with(
	person_1 varchar2(30),
	person_2 varchar2(30),
	primary key(person_1, person_2),
	foreign key(person_1) references Users on delete cascade,
	foreign key(person_2) references Users on delete cascade
);

create table SecurityQuestions(
	q_id integer primary key,
	question varchar2(100),
	answer varchar2(30),
	username varchar2(30) not null,
	foreign key(username) references Users on delete cascade
);

create table Events(
	e_id integer primary key,
	name varchar2(100),
	description varchar2(1000),
	dateof date,
	event_img image
);

create table favorited(
	username varchar2(30),
	e_id integer,
	primary key(username, e_id),
	foreign key(username) references Users on delete cascade,
	foreign key(e_id) references Events
);

create table Tags(
	tag_name varchar2(50),
	primary key(tag_name),
	constraint bad_tags
	-- check constraint for curse words
	check (tag_name not in ('ass', 'shit', 'fuck'))
);

create table tagged_with(
	tag_name varchar2(50),
	e_id integer,
	primary key(tag_name, e_id),
	foreign key(tag_name) references Tags,
	foreign key(e_id) references Events
);

create table Locations(
	l_id integer,
	name varchar2(50),
	address varchar2(50),
	directions varchar2(200),
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
	on_or_off number(1) check (on_or_off = 0 or on_or_off = 1),
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
	username varchar2(30),
	p_id integer,
	primary key(username, p_id),
	foreign key(username) references Users on delete cascade,
	foreign key(p_id) references Preferences on delete cascade
);
