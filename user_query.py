import psycopg2
import json
import config

'''
	user_query.py
	author: Tao Liu and Xi Chen
	This Query class connects to the user table and provides functions for app.py
'''

class UserQuery:
	def __init__(self):
		pass

	def connect_to_db(self):
		"""
			Connect to the database
	    """
		# connection = psycopg2.connect(database=config.database, user=config.user, password= config.password)
		connection = psycopg2.connect(database=config.database, user=config.user)
		return connection

	def check_if_user_exist(self, id):
		"""
	    Check if an user exists in the users table
	    :param id: the id of the user
	    :return: true if the user exists, false if not
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select * from users where user_id=%d;''' % (id))
		length = len(cursor.fetchall())
		connection.close()
		return length == 1

	def add_user(self, id, name):
		"""
	    Add an user to the users table
	    :param id: the id of the user
	     	   name: the name of the user
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()

		cursor.execute("insert into users values (%s, %s, %s, %s);", (id,name, '{}', '{}'))
		connection.commit()
		connection.close()

	def update_user_preference(self, id, genres, movies):
		"""
	    Update user's preference to the users table
	    :param id: the id of the user
	     	   genres: the genres that the user has chosen
	     	   movies: the movies that the user has chosen
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		
		genre_str = "{"
		for gen in genres:
			genre_str += gen.lower() + ","
		genre_str = genre_str[0:-1] + "}"

		movie_str = "{"
		for movie in movies:
			movie_str += movie.lower() + ","
		movie_str = movie_str[0:-1] + "}"	
		
		query = '''update "users" set "selected_genres" = '%s\', "selected_movies" = '%s\' where "user_id" = %d;''' %(genre_str, movie_str, id)
		cursor.execute(query)
		connection.commit()
		connection.close()

	def find_user_by_id(self, id):
		"""
	    Find a user's information by id
	    :param id: the id of the user
	    :return: a dictionary which describes one user with keys "user_id", 
	    		 "user_name", "selected_genres", "selected_movies"
	    """
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute("select * from users where user_id=%d;" % (id))
		row = cursor.fetchone()
		connection.close()
		return self.convert_to_json(row)


	def convert_to_json(self, row):
		"""
	    Convert rows into json list
	    :param rows: each row contains information of a user
	    :return: a dictionary which describes one user with keys "user_id", 
	    		 "user_name", "selected_genres", "selected_movies"
	    """
		json_record = {}
		json_record["user_id"] = row[0]
		json_record["user_name"] = row[1]
		json_record["selected_genres"] = row[2]
		json_record["selected_movies"] = row[3]
		return json.dumps(json_record, indent = 4)
		

if __name__ == "__main__":
	user_query = UserQuery()
	user_id = 1733123836910484
	user_query.update_user_preference(user_id, ["crime", "romance"], ["loli", "pop"])
	user_obj = json.loads(user_query.find_user_by_id(user_id))
	print user_obj["selected_genres"]

