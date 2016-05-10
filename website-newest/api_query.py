#!/usr/bin/env python
import psycopg2
import json
from math import ceil
import string
import re
'''
	api_query.py
	author: Tao Liu and Xi Chen
	This Query class wraps the details of the API query for api.py, which will call methods
	implemented in api_query.py.
'''

def titlecase(s):
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
		#connection = psycopg2.connect(database="liut2", user="liut2", password="heart724barn")
		connection = psycopg2.connect(database="movie", user="postgres")
		return connection

	def get_recent_release_for_page(self, page,PER_PAGE):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (page - 1) * 15
		cursor.execute('''select * from movies where release_year = 2016 order by weighted desc limit %d offset %d;''' % (PER_PAGE, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_recent_release_with_count(self):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies where release_year = 2016;''')
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count))
		return page_count

	def get_favourite_from_year_count(self, year):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies where release_year = %d;''' % (year))
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count))
		return page_count

	def get_favourite_from_year_for_page(self, year,page,PER_PAGE):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (page - 1) * 15
		cursor.execute('''select * from movies where release_year = %d order by weighted desc limit %d offset %d;''' % (year, PER_PAGE, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_with_count(self):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies;''')
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count))
		return page_count

	def get_toprated_for_page(self, page,PER_PAGE):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (page - 1) * 15
		cursor.execute('''select * from movies order by weighted desc limit %d offset %d;''' % (PER_PAGE, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_in_genre(self, genre, first_n):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select * from movies where genres && '{%s}'::varchar(100)[] order by weighted desc limit %d;''' % (genre, first_n))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_in_genre_for_page(self, genre,page,PER_PAGE):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		offset = (page - 1) * 15
		cursor.execute('''select * from movies where genres && '{%s}'::varchar(100)[] order by weighted desc limit %d offset %d;''' % (genre,PER_PAGE, offset))
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_toprated_in_genre_with_count(self, genre):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies where genres && '{%s}'::varchar(100)[];''' % (genre))
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count))
		return page_count

	def get_movies_containing_title(self, string):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select * from movies where title::varchar(500) like '% {0}%' OR title::varchar(500) like '% {0} %' OR title::varchar(500) like '{0} %' OR title::varchar(500) like '{0}' OR title::varchar(500) like '% {0}';'''.format(string))		
		rows = cursor.fetchall()
		connection.close()
		return self.convert_to_json(rows)

	def get_movies_containing_title_with_count(self, string):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select count(*) from movies where (title::varchar(500) like '% {0}%' OR title::varchar(500) like '% {0} %' OR title::varchar(500) like '{0} %' OR title::varchar(500) like '{0}' OR title::varchar(500) like '% {0}');'''.format(string))		
		page_count =  cursor.fetchone()[0]
		connection.close()
		page_count = int(ceil(page_count))
		return page_count

	def convert_to_json(self, rows):
		json_list = []
		for row in rows:
			json_record = {}
			json_record["movie_id"] = row[0]
			json_record["title"] = titlecase(row[1])
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

