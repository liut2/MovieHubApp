create table users
	(user_id	bigint,
	 user_name	varchar(100),
	 selected_genres varchar(100)[],
	 selected_movies varchar(200)[],
	 primary key(user_id));