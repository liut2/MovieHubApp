#!/usr/bin/env python
import psycopg2
import json
from math import ceil
import string
import re
import config
'''
	api_query.py
	author: Tao Liu and Xi Chen
	This Query class wraps the details of the API query for api.py, which will call methods
	implemented in api_query.py.
'''

def change_title(s):
	"""
    Transform the lowercase title into title with upper initials
    :param s: the title to be transformed
    :return: title with upper intials
    """
	s = re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
              lambda mo: mo.group(0)[0].upper() +
                          mo.group(0)[1:].lower(),s)
	s = s.split(" ")
	for i in range(len(s)):
		if (s[i] in "Ii Iii Iv Vi Vii Viii Ix Ii: Iii: Iv: Vi: Vii: Viii: Ix:"):
			s[i] = s[i].upper()
	return " ".join(s)

class MovieQuery:
	def __init__(self):
		pass

	def connect_to_db(self):
		"""
		Connect to the database indicated by the config file
	    """
		# connection = psycopg2.connect(database=config.database, user=config.user,password = config.password)
		connection = psycopg2.connect(database=config.database, user=config.user)
		return connection

	def get_recent_release_for_page(self, page, PER_PAGE):
		"""
	    Get a page of recent released movies
	    :param page: the index of the page. e.g. page = 1 represents the first page
	    	   PER_PAGE: the number of movies on one page
	    :return: a list of dictionary, each of which describes one movie with keys "movie_id", "title", 
	    "genres", "imdb_id", "tmdb_id", "rating", "number_of_ratings", "weighted_rating", "release_year", 
	    "img_path", "description", "director", "length" 
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (page - 1) * 15
		cursor.execute('''select * from movies where release_year = 2016 order by weighted desc limit %d offset %d;''' % (PER_PAGE, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_recent_release_with_count(self):
		"""
	    Count the total number of recent released movies
	    :return: the number of recent released movies
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies where release_year = 2016;''')
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count))
		return page_count

	def get_favourite_from_year_with_count(self, year):
		"""
	    Count the total number of movies in the year indicated by the parameter
	    :para: year: the year that the user want to see
	    :return: the number of movies in the year indicated by the parameter
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies where release_year = %d;''' % (year))
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count))
		return page_count

	def get_favourite_from_year_for_page(self, year, page, PER_PAGE):
		"""
	    Get a page of movies in a particular year
	    :param year: the year that the user want to see
	    :return: a list of dictionary, each of which describes one movie with keys "movie_id", "title", 
	    "genres", "imdb_id", "tmdb_id", "rating", "number_of_ratings", "weighted_rating", "release_year", 
	    "img_path", "description", "director", "length" 
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (page - 1) * 15
		cursor.execute('''select * from movies where release_year = %d order by weighted desc limit %d offset %d;''' % (year, PER_PAGE, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_with_count(self):
		"""
	    Count the total number of movies
	    :return: the number of movies in the database
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies;''')
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count))
		return page_count

	def get_toprated_for_page(self, page, PER_PAGE):
		"""
	    Get a page of toprated movies 
	    :param page: the index of the page. e.g. page = 1 represents the first page
	    	   PER_PAGE: the number of movies on one page
	    :return: a list of dictionary, each of which describes one movie with keys "movie_id", "title", 
	    "genres", "imdb_id", "tmdb_id", "rating", "number_of_ratings", "weighted_rating", "release_year", 
	    "img_path", "description", "director", "length" 
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (page - 1) * 15
		cursor.execute('''select * from movies order by weighted desc limit %d offset %d;''' % (PER_PAGE, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_in_genre(self, genre, first_n):
		"""
	    Get a list of toprated movies in a particular genre
	    :para: genre: one of ['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir',
	    	          'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action',
	    	          'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax']
	    	   first_n: the number of movies that will be returned
	    :return: a list of dictionary, each of which describes one movie with keys "movie_id", "title", 
	    "genres", "imdb_id", "tmdb_id", "rating", "number_of_ratings", "weighted_rating", "release_year", 
	    "img_path", "description", "director", "length" 
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select * from movies where genres && '{%s}'::varchar(100)[] order by weighted desc limit %d;''' % (genre, first_n))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_in_genre_for_page(self, genre, page, PER_PAGE):
		"""
	    Get a page of movies of a particular genre
	    :param page: the index of the page. e.g. page = 1 represents the first page
	    	   PER_PAGE: the number of movies on one page
	    	   genre: one of ['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir',
	    	          'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action',
	    	          'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax']
	    :return: a list of dictionary, each of which describes one movie with keys "movie_id", "title", 
	    "genres", "imdb_id", "tmdb_id", "rating", "number_of_ratings", "weighted_rating", "release_year", 
	    "img_path", "description", "director", "length" 
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (page - 1) * 15
		cursor.execute('''select * from movies where genres && '{%s}'::varchar(100)[] order by weighted desc limit %d offset %d;''' % (genre,PER_PAGE, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_in_genre_with_count(self, genre):
		"""
	    Count the total number of movies in a particular genre
	    :genre para: one of ['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir',
	    	          'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action',
	    	          'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax']
	    :return: the number of movies in a particular genre
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies where genres && '{%s}'::varchar(100)[];''' % (genre))
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count))
		return page_count

	def get_movies_containing_title(self, string):
		"""
	    Get a list of movies that matches the string
	    :param string: the word that the user want to search
	    :return: a list of dictionary, each of which describes one movie with keys "movie_id", "title", 
	    "genres", "imdb_id", "tmdb_id", "rating", "number_of_ratings", "weighted_rating", "release_year", 
	    "img_path", "description", "director", "length" 
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select * from movies where title::varchar(500) like '% {0}%' OR title::varchar(500) like '% {0} %' OR title::varchar(500) like '{0} %' OR title::varchar(500) like '{0}' OR title::varchar(500) like '% {0}';'''.format(string))		
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_movies_by_id(self, arr):
		"""
	    Get a list of movies indicated by the array containing indexes
	    :param arr: an array of movie indexes
	    :return: a list of dictionary, each of which describes one movie with keys "movie_id", "title", 
	    "genres", "imdb_id", "tmdb_id", "rating", "number_of_ratings", "weighted_rating", "release_year", 
	    "img_path", "description", "director", "length" 
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		result_list = []
		for movie_id in arr:
			movie_id = int(movie_id)
			cursor.execute("select * from movies where movie_id = %d;" % (movie_id))
			row = cursor.fetchone()
			result_list.append(row)
		connection.close()
		return self.convert_to_json(result_list)


	def convert_to_json(self, rows):
		"""
	    Convert rows into json list
	    :param rows: each row contains information of a movie
	    :return: a list of dictionary, each of which describes one movie with keys "movie_id", "title", 
	    "genres", "imdb_id", "tmdb_id", "rating", "number_of_ratings", "weighted_rating", "release_year", 
	    "img_path", "description", "director", "length" 
	    """
		json_list = []
		for row in rows:
			json_record = {}
			json_record["movie_id"] = row[0]
			json_record["title"] = change_title(row[1])
			json_record["genres"] = row[2]
			json_record["imdb_id"] = row[3]
			json_record["tmdb_id"] = row[4]
			json_record["rating"] = row[5]
			json_record["number_of_ratings"] = row[6]
			json_record["weighted_rating"] = row[7]
			json_record["release_year"] = row[8]
			json_record["img_path"] = row[9]
			json_record["description"] = row[10]
			json_record["director"] = row[11]
			json_record["length"] = row[12]
			json_list.append(json_record)
		return json.dumps(json_list, indent = 4)


