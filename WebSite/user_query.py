import psycopg2
import json

class UserQuery:
	def __init__(self):
		pass

	def connect_to_db(self):
		connection = psycopg2.connect(database="movie", user="postgres")
		return connection

	def check_if_user_exist(self, id):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute('''select * from users where user_id=%d;''' % (id))
		length = len(cursor.fetchall())
		connection.close()
		return length == 1

	def add_user(self, id, name):
		connection = self.connect_to_db()
		cursor = connection.cursor()

		cursor.execute("insert into users values (%s, %s, %s, %s);", (id,name, '{}', '{}'))
		connection.commit()
		connection.close()

	def update_user_preference(self, id, genres, movies):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		'''
		genre_str = "{"
		for gen in genres:
			genre_str += gen.lower() + ","
		genre_str = genre_str[0:-1] + "}"

		movie_str = "{"
		for movie in movies:
			movie_str += movie.lower() + ","
		movie_str = movie_str[0:-1] + "}"
		'''
		
		genres = str(map(str, genres))
		genres = genres.replace('[', '{').replace(']', '}').replace('\'', '\"')

		movies = str(map(str, movies))
		movies = movies.replace('[', '{').replace(']', '}').replace('\'', '\"')		
		
		query = '''update "users" set "selected_genres" = '%s\', "selected_movies" = '%s\' where "user_id" = %d;''' %(genres, movies, id)
		cursor.execute(query)
		connection.commit()
		connection.close()

	def find_user_by_id(self, id):
		connection = self.connect_to_db()
		cursor = connection.cursor()
		cursor.execute("select * from users where user_id=%d;" % (id))
		row = cursor.fetchone()
		connection.close()
		return self.convert_to_json(row)


	def convert_to_json(self, row):
		json_record = {}
		json_record["user_id"] = row[0]
		json_record["user_name"] = row[1]
		json_record["selected_genres"] = row[2]
		json_record["selected_movies"] = row[3]
		return json.dumps(json_record, indent = 4)
		

if __name__ == "__main__":
	user_query = UserQuery()
	user_id = 1733123836910484
	#if not user_query.check_if_user_exist(user_id):
	#	print "not exist yet"
	#	user_query.add_user(user_id, 'Tao Liu', ["crime", "romance"], ["loli", "pop"])
	#print user_query.check_if_user_exist(user_id)

	#print user_query.find_user_by_id(user_id)
	user_query.update_user_preference(user_id, ["crime", "romance"], ["loli", "pop"])
	user_obj = json.loads(user_query.find_user_by_id(user_id))
	print user_obj["selected_genres"]

