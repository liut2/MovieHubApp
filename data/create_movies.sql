create table movies
	(movie_id	int,
	 title		varchar(500),
	 genres		varchar(100)[],
	 imdb_id	int,
	 tmdb_id	int,
	 rating		float(1),
	 number_of_ratings	int,
	 weighted	float(1),
	 release_year	int,
	 primary key(movie_id));
