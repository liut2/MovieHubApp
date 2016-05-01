import psycopg2

class UserQuery:
	def __init__(self):
		pass

	def connect_to_db(self):
		connection = psycopg2.connect(database="movie_app", user="taoliu")
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
		cursor.execute("insert into users values (%s, %s);", (id,name))
		connection.commit()
		connection.close()


if __name__ == "__main__":
	user_query = UserQuery()
	user_id = 1733123836910484
	if not user_query.check_if_user_exist(user_id):
		print "not exist yet"
		user_query.add_user(user_id, 'Tao Liu')
	print user_query.check_if_user_exist(user_id)

