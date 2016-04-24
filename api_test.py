#author: Tao Liu and Chen Xi
import unittest
import requests
import json
'''
This api_test contains 34 tests cases for our movie app. It covers all of typical 
and edge cases we can think of for this HTTP based web API.
'''
class MovieQueryTester(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	# test the main page
	def test_main(self):
		# return a list of countries that is available
		url = "http://localhost:5000/"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server,"meow meow")

	# test the top_rated function
	def test_top_rated_typical(self):
		url = "http://localhost:5000/topratedmovies/1"
		data_from_server = requests.get(url).text
		received_data = json.loads(data_from_server)
		expected_data = [ { "rating": 4.44, "genres": [ "crime", "drama" ], "movie_id": 318, "release_year": 1994, "tmdb_id": 278, "title": "shawshank redemption, the ", "number_of_ratings": 77887, "imdb_id": 111161, "weighted_rating": 4.423 } ]
		self.assertEqual(received_data,expected_data)
		

	def test_top_rated_empty(self):
		url = "http://localhost:5000/topratedmovies/0"
		data_from_server = requests.get(url).text
		received_data = json.loads(data_from_server)
		self.assertEqual(received_data,[])

	def test_top_rated_null(self):
		url = "http://localhost:5000/topratedmovies/"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server, "Page not found.")

	def test_top_rated_invalid_number_too_high(self):
		url = "http://localhost:5000/topratedmovies/40000"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server,"Please enter a valid url for toprated movies query.")

	def test_top_rated_invalid_not_a_number(self):
		url = "http://localhost:5000/topratedmovies/meow"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server,"Page not found.")

	def test_top_rated_invalid_negative_number(self):
		url = "http://localhost:5000/topratedmovies/-1"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server,"Page not found.")

	def test_top_rated_invalid4_other_ascii_letters(self):
		url = "http://localhost:5000/topratedmovies/!@#"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server,"Page not found.")

	# test favorite from a year
	def test_favorite_from_year_typical1(self):
		url = "http://localhost:5000/2015/toppicks/2"
		data_from_server = requests.get(url).text
		received_data = json.loads(data_from_server)
		expected_data = [{"rating": 4.02, "genres": ["animation", "children", "comedy"], "movie_id": 134853, "release_year": 2015, "tmdb_id": 150540, "title": "inside out ", "number_of_ratings": 4360, "imdb_id": 2096673, "weighted_rating": 3.8481}, {"rating": 4.06, "genres": ["action", "adventure", "sci-fi"], "movie_id": 134130, "release_year": 2015, "tmdb_id": 286217, "title": "martian, the ", "number_of_ratings": 3277, "imdb_id": 3659388, "weighted_rating": 3.8353}]
		self.assertEqual(received_data, expected_data)

	def test_favorite_from_year_typical2(self):
		url = "http://localhost:5000/1995/toppicks/1"
		data_from_server = requests.get(url).text
		received_data = json.loads(data_from_server)
		expected_data = [{"rating": 4.32, "genres": ["crime", "mystery", "thriller"], "movie_id": 50, "release_year": 1995, "tmdb_id": 629, "title": "usual suspects, the ", "number_of_ratings": 53195, "imdb_id": 114814, "weighted_rating": 4.2975}]
		self.assertEqual(received_data, expected_data)

	def test_favorite_from_year_empty(self):
		url = "http://localhost:5000/1995/toppicks/0"
		data_from_server = requests.get(url).text
		movie_list = json.loads(data_from_server)
		self.assertEqual(movie_list,[])

	def test_favorite_from_year_null(self):
		url = "http://localhost:5000/1995/toppicks/"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server,"Page not found.")

	def test_favorite_from_year_invalid1_year_too_low(self):
		url = "http://localhost:5000/1772/toppicks/10"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server,"Please enter a valid url for get favourite movies from year query.")

	def test_favorite_from_year_invalid2_negative_number(self):
		url = "http://localhost:5000/2015/toppicks/-2"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server,"Page not found.")

	def test_favorite_from_year_invalid3_negative_year(self):
		url = "http://localhost:5000/-5/toppicks/2"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server,"Page not found.")

	def test_favorite_from_year_invalid4_other_ascii_letters(self):
		url = "http://localhost:5000/2014/toppicks/#@!"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server, "Page not found.")

	# test recent_release
	def test_recent_release_typical1(self):
		url = "http://localhost:5000/recentrelease/1"
		data_from_server = requests.get(url).text
		received_data = json.loads(data_from_server)
		expected_data = [{"rating": 3.75, "genres": ["action", "crime", "drama", "mystery", "thriller"], "movie_id": 150548, "release_year": 2016, "tmdb_id": 370646, "title": "sherlock: the abominable bride ", "number_of_ratings": 151, "imdb_id": 3845232, "weighted_rating": 3.1843}]
		self.assertEqual(received_data, expected_data)

	def test_recent_release_empty(self):
		url = "http://localhost:5000/recentrelease/0"
		data_from_server = requests.get(url).text
		movie_list = json.loads(data_from_server)
		self.assertEqual(movie_list, [])

	def test_recent_release_null(self):
		url = "http://localhost:5000/recentrelease/"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server, "Page not found.")

	def test_recent_release_invalid1_nagative_number(self):
		url = "http://localhost:5000/recentrelease/-5"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server, "Page not found.")

	def test_recent_release_invalid2_other_ascii_letter(self):
		url = "http://localhost:5000/recentrelease/&*&"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server, "Page not found.")

	# test top rated in genre
	def test_toprated_in_genre_typical1(self):
		url = "http://localhost:5000/horror/2"
		data_from_server = requests.get(url).text
		received_data = json.loads(data_from_server)
		expected_data = [{"rating": 4.16, "genres": ["crime", "horror", "thriller"], "movie_id": 593, "release_year": 1991, "tmdb_id": 274, "title": "silence of the lambs, the ", "number_of_ratings": 76271, "imdb_id": 102926, "weighted_rating": 4.1463}, {"rating": 4.07, "genres": ["crime", "horror"], "movie_id": 1219, "release_year": 1960, "tmdb_id": 539, "title": "psycho ", "number_of_ratings": 21198, "imdb_id": 54215, "weighted_rating": 4.0263}]
		self.assertEqual(received_data, expected_data)

	def test_toprated_in_genre_upper_case_genre(self):
		url = "http://localhost:5000/Animation/1"
		data_from_server = requests.get(url).text
		received_data = json.loads(data_from_server)
		expected_data = [{"rating": 4.19, "genres": ["adventure", "animation", "fantasy"], "movie_id": 5618, "release_year": 2001, "tmdb_id": 129, "title": "spirited away (sen to chihiro no kamikakushi) ", "number_of_ratings": 16830, "imdb_id": 245429, "weighted_rating": 4.1288}]
		self.assertEqual(received_data, expected_data)

	def test_toprated_in_genre_empty(self):
		url = "http://localhost:5000/drama/0"
		data_from_server = requests.get(url).text
		movie_list = json.loads(data_from_server)
		self.assertEqual(movie_list, [])

	def test_toprated_in_genre_invalid_null_number(self):
		url = "http://localhost:5000/drama/"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server, "Page not found.")

	def test_toprated_in_genre_invalid_null_genre(self):
		url = "http://localhost:5000/132"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server, "Page not found.")

	def test_toprated_in_genre_invalid4(self):
		url = "http://localhost:5000/sfdwere/rwe"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server, "Page not found.")

	def test_toprated_in_genre_invalid5(self):
		url = "http://localhost:5000/drama/12ds"
		data_from_server = requests.get(url).text
		self.assertEqual(data_from_server, "Page not found.")

	# test title contains function
	def test_title_contains_typical1(self):
		url = "http://localhost:5000/titlecontains?query=the+revenant"
		data_from_server = requests.get(url).text
		received_data = json.loads(data_from_server)
		expected_data = [{"rating": 3.93, "genres": ["adventure", "drama"], "movie_id": 139385, "release_year": 2015, "tmdb_id": 281957, "title": "the revenant ", "number_of_ratings": 446, "imdb_id": 1663202, "weighted_rating": 3.3552}]
		self.assertEqual(received_data, expected_data)

	def test_title_contains_typical3(self):
		url = "http://localhost:5000/titlecontains?query=avatar"
		data_from_server = requests.get(url).text
		received_data = json.loads(data_from_server)
		expected_data = [{"rating": 3.73, "genres": ["action", "adventure", "sci-fi", "imax"], "movie_id": 72998, "release_year": 2009, "tmdb_id": 19995, "title": "avatar ", "number_of_ratings": 14555, "imdb_id": 499549, "weighted_rating": 3.6894}]
		self.assertEqual(received_data, expected_data)

	def test_title_contains_not_valid_title(self):
		url = "http://localhost:5000/titlecontains?query=sfdjlkwejrwlerk1213r"
		data_from_server = requests.get(url).text
		movie_list = json.loads(data_from_server)
		self.assertEqual(movie_list, [])

	def test_title_contains_invalid1(self):
		url = "http://localhost:5000/titlecontains?"
		data_from_server = requests.get(url).text
		movie_list = json.loads(data_from_server)
		self.assertEqual(movie_list, [])

	def test_title_contains_invalid2(self):
		url = "http://localhost:5000/titlecontains"
		data_from_server = requests.get(url).text
		movie_list = json.loads(data_from_server)
		self.assertEqual(movie_list, [])

	def test_title_contains_invalid3(self):
		url = "http://localhost:5000/titlecontains?dswe"
		data_from_server = requests.get(url).text
		movie_list = json.loads(data_from_server)
		self.assertEqual(movie_list, [])


if __name__ == '__main__':
	unittest.main()
