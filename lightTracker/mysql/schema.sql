-- Database name: lighttracker

drop table tLightRuns;
create table if not exists tLightRuns (
	run_id  int unsigned auto_increment primary key,
	cr_date timestamp default current_timestamp on update current_timestamp
);

drop table tLightValues;
create table if not exists tLightValues (
	val_id 	int unsigned auto_increment primary key,
	run_id  int unsigned,
	value   int,
	cr_date timestamp default current_timestamp on update current_timestamp,
	foreign key (run_id) references tLightRuns(run_id)
);
