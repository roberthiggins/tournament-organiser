create table game{
	id integer serial primary key unique,
	entry_1 integer references entry(id),
	entry_2 integer references entry(id),
	round_num integer,
	tourn varchar reference tournament(name),
	entry_1_score json,
	entry_2_score json,
	table_num integer
};
