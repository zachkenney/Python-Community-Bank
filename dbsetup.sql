create table bank.users (
	id SERIAL primary key,
	first_name varchar(50) not null,
	last_name varchar(50) not null,
	username varchar(16) not null,
	pwd varchar(16) not null
);

CREATE TABLE bank.accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES bank.users(id),
    account_type varchar(16) not null,
    balance decimal(10,2) not null
);