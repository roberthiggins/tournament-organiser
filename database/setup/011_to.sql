create table organiser (
	id integer references account(id),
	username varchar not null unique,
	settings json
);
