#!/usr/bin/env python
import psycopg2
import json
from math import ceil
'''
	api_query.py
	author: Tao Liu and Xi Chen
	This Query class wraps the details of the API query for api.py, which will call methods
	implemented in api_query.py.
'''
class MovieQuery:
	def __init__(self):
		pass

	def connect_to_db(self):
		#connection = psycopg2.connect(database="liut2", user="liut2", password="heart724barn")
		connection = psycopg2.connect(database="movie_app", user="taoliu")
		return connection

	def get_recent_release(self, first_n):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select * from movies where release_year = 2016 order by weighted desc limit %d;''' % (first_n))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_recent_release_with_pagination(self, limit, nth_page):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (nth_page - 1) * limit
		cursor.execute('''select * from movies where release_year = 2016 order by weighted desc limit %d offset %d;''' % (limit, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_recent_release_with_page_count(self, limit):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies where release_year = 2016;''')
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count / (1.0*limit)))
		return page_count

	def get_favourite_from_year(self, year, first_n):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select * from movies where release_year = %d order by weighted desc limit %d;''' % (year, first_n))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_favourite_from_year_with_pagination(self, year, limit, nth_page):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (nth_page - 1) * limit
		cursor.execute('''select * from movies where release_year = %d order by weighted desc limit %d offset %d;''' % (year, limit, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_favourite_from_year_with_page_count(self, year, limit):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies where release_year = %d;''' % (year))
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count / (1.0*limit)))
		return page_count

	def get_toprated(self, first_n):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select * from movies order by weighted desc limit %d;''' % (first_n))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_with_pagination(self, limit, nth_page):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (nth_page - 1) * limit
		cursor.execute('''select * from movies order by weighted desc limit %d offset %d;''' % (limit, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_with_page_count(self, limit):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies;''')
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count / (1.0*limit)))
		return page_count

	def get_toprated_in_genre(self, genre, first_n):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select * from movies where genres && '{%s}'::varchar(100)[] order by weighted desc limit %d;''' % (genre, first_n))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_in_genre_with_pagination(self, genre, limit, nth_page):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (nth_page - 1) * limit
		cursor.execute('''select * from movies where genres && '{%s}'::varchar(100)[] order by weighted desc limit %d offset %d;''' % (genre, limit, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_in_genre_with_page_count(self, genre, limit):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies where genres && '{%s}'::varchar(100)[];''' % (genre))
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count / (1.0*limit)))
		return page_count

	def get_movies_containing_title(self, string):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select * from movies where title::varchar(500) like '%{0}%';'''.format(string))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def convert_to_json(self, rows):
		json_list = []
		for row in rows:
			json_record = {}
			json_record["movie_id"] = row[0]
			json_record["title"] = row[1].title()
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


if __name__ == "__main__":
	query = MovieQuery()
	genres = ['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir', 'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action', 'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax']
	#print query.get_favourite_from_year_with_pagination(2015, 3, 1)
	print query.get_favourite_from_year(2015, 3)
	#print query.get_favourite_from_year_with_page_count(2015, 10)
	#print query.get_toprated_in_genre_with_page_count('crime', 10)
	#query.get_recent_release(10)
	#query.get_favourite_from_year(2015, 10)
	#query.get_toprated(10)
	#query.get_toprated_in_genre("Crime", 10)
	#query.get_movies_containing_title("father")
