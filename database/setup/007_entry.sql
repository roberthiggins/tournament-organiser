create table entry (
	id 		serial not null unique,
	tournament_id   varchar unique references tournament(name),
	is_accepted	bool not null 
);
-- Why do we need is_accepted? The registration gets finalised. An entry assumes accepted I would suppose.
