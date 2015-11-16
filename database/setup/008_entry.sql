create table entry{
	id 		integer serial not null  unique,
	tourn_name	varchar unique references tournament(name),
	is_accepted	bool not null 
};
