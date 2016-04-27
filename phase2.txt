Author: Xi Chen and Tao Liu


#this table contains the info about a movie from movielens project
create table movies
        (movie_id  	       int,
         title                 varchar(500),
         genres    	       varchar(100)[],
         imdb_id   	       int,
         tmdb_id   	       int,
         rating                float(1),
         number_of_ratings     int,
         weighted_rating       float(1),
         release_year          int,
         primary key(movie_id));


SYNOPSIS:  Get the first n top rated movies in the whole database.
QUERY  (GET):  /topratedmovies/<int:n>
RESPONSE:  A list of movie objects, each of which contains the meta description of it, such as title, rating, and  released year.
EXAMPLE:  http://thacker.mathcs.carleton.edu:5128/topratedmovies/2
[ { "rating": 4.44, "genres": [ "crime", "drama" ], "movie_id": 318, "release_year": 1994, "tmdb_id": 278, "title": "shawshank redemption, the ", "number_of_ratings": 77887, "imdb_id": 111161, "weighted_rating": 4.423 }, { "rating": 4.35, "genres": [ "crime", "drama" ], "movie_id": 858, "release_year": 1972, "tmdb_id": 238, "title": "godfather, the ", "number_of_ratings": 49846, "imdb_id": 68646, "weighted_rating": 4.3254 } ]
 


SYSNOPSIS: Get the first n toprated movies from year xxxx.
QUERY  (GET) /<int:year>/toppicks/<int:n>
RESPONSE:  A list of movie objects in year m, each of which contains the meta description of it, such as title, rating, and  released year.
EXAMPLE:  http://thacker.mathcs.carleton.edu:5128/2016/toppicks/1
[ { "rating": 3.75, "genres": [ "action", "crime", "drama", "mystery", "thriller" ], "movie_id": 150548, "release_year": 2016, "tmdb_id": 370646, "title": "sherlock: the abominable bride ", "number_of_ratings": 151, "imdb_id": 3845232, "weighted_rating": 3.1843 } ]


SYSNOPSIS: Get the first n movies in recent release.
QUERY  (GET) /recentrelease/<int:n>
RESPONSE:  A list of movie objects in year m, each of which contains the meta description of it, such as title, rating, and  released year.
EXAMPLE:  http://thacker.mathcs.carleton.edu:5128/recentrelease/1
[ { "rating": 3.75, "genres": [ "action", "crime", "drama", "mystery", "thriller" ], "movie_id": 150548, "release_year": 2016, "tmdb_id": 370646, "title": "sherlock: the abominable bride ", "number_of_ratings": 151, "imdb_id": 3845232, "weighted_rating": 3.1843 } ]


SYSNOPSIS: Get a list of movies whose title contains the search string
QUERY  (GET) /titlecontains
RESPONSE:  A list of movie objects, each of which contains the meta description of it, such as title, rating, and  released year.
EXAMPLE:  http://thacker.mathcs.carleton.edu:5128/titlecontains?query=the+revenant
[ { "rating": 3.93, "genres": [ "adventure", "drama" ], "movie_id": 139385, "release_year": 2015, "tmdb_id": 281957, "title": "the revenant ", "number_of_ratings": 446, "imdb_id": 1663202, "weighted_rating": 3.3552 } ]


SYSNOPSIS: Get a list of first n top rated movies in a specific genre.
QUERY  (GET) /<genre>/<int:n>
RESPONSE:  A list of movie objects, each of which contains the meta description of it, such as title, rating, and  released year.
EXAMPLE:  http://thacker.mathcs.carleton.edu:5128/crime/3
[ { "rating": 4.44, "genres": [ "crime", "drama" ], "movie_id": 318, "release_year": 1994, "tmdb_id": 278, "title": "shawshank redemption, the ", "number_of_ratings": 77887, "imdb_id": 111161, "weighted_rating": 4.423 }, { "rating": 4.35, "genres": [ "crime", "drama" ], "movie_id": 858, "release_year": 1972, "tmdb_id": 238, "title": "godfather, the ", "number_of_ratings": 49846, "imdb_id": 68646, "weighted_rating": 4.3254 }, { "rating": 4.32, "genres": [ "crime", "mystery", "thriller" ], "movie_id": 50, "release_year": 1995, "tmdb_id": 629, "title": "usual suspects, the ", "number_of_ratings": 53195, "imdb_id": 114814, "weighted_rating": 4.2975 } ]