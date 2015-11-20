create table to{
	id integer references account(id);
	username varchar not null unique;
	settings json
};
