import psycopg2
import json
import config
import collections

class Recommender:
	def __init__(self):
		pass

	def connect_to_db(self):
		connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
		# connection = psycopg2.connect(database=config.database, user=config.user)
		return connection

	def query_movie(self, arr):
		connection = self.connect_to_db()
		cursor = connection.cursor()

		for movie_id in arr:
			movie_id = int(movie_id)
			cursor.execute("select title from movies where movie_id = %d;" % (movie_id))
			row = cursor.fetchone()
			print row

		connection.close()
		
	def find_movie_for_you(self, arr, n):
		connection = self.connect_to_db()
		cursor = connection.cursor()

		similarity_count_dict = {}
		# first pass, find top n users of similar tastes with you
		for movie_id in arr:
			movie_id = int(movie_id)
			cursor.execute("select user_list from movie_to_user where movie_id = %d;" % (movie_id))
			row = cursor.fetchone()
			
			if row == None:
				continue
			
			for user_id in row[0]:
				user_id = int(user_id)
				if user_id not in similarity_count_dict:
					similarity_count_dict[user_id] = 1
				else:
					similarity_count_dict[user_id] += 1
		#sort dict by value
		i = 0
		top_similar = []
		for key in sorted(similarity_count_dict, key=similarity_count_dict.get, reverse=True):
			i = i + 1
  			print key, similarity_count_dict[key]
  			top_similar.append(key)
  			print " "
  			if i == n:
  				break
  		
  		#second pass, find intersection of top taste users
  		cursor.execute("select movie_list from user_to_movie where user_id = %d;" % (top_similar[0]))
		row = cursor.fetchone()
  		prev = set(row[0])
  		cur = []
  		for i in range(1, len(top_similar)):
  			user_id = top_similar[i]
  			cursor.execute("select movie_list from user_to_movie where user_id = %d;" % (user_id))
			row = cursor.fetchone()
			cur = row[0]
			prev = prev.intersection(cur)

		connection.close()
		result = []
		for movie_id in list(prev):
			movie_id = int(movie_id)
			if movie_id not in arr:
				result.append(movie_id)
		return result



if __name__ == "__main__":
	recommender = Recommender()
	#recommender.convert_title_to_id(["Inception", "The Matrix", "Pulp Fiction", "North By Northwest", "City Of God", "Zootopia", "Rear Window", "The Dark Knight"])
	arr = recommender.find_movie_for_you(["5971", "58559", "60069", "6016", "260", "908", "5618", "4973", "296", "151715"],3)
	recommender.query_movie(arr)


