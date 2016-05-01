create table movies
	(movie_id	int,
	 title		varchar(200),
	 genres		varchar(100)[],
	 imdb_id	int,
	 tmdb_id	int,
	 rating		float(1),
	 number_of_ratings	int,
	 weighted	float(1),
	 release_year	int,
	 img_path	varchar(300),
	 description varchar(600),
	 director	varchar(100),
	 length	varchar(20),
	 primary key(movie_id));
	 
