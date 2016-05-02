#!/usr/bin/env python
'''
	api.py, written in python 2
	author: Tao Liu and Xi Chen
	This is an HTTP based API for quering movie ratings data,
	with error handling if route is not found; otherwise returning
	the data in json format.
'''
import flask
import json
from flask import request
from api_query import MovieQuery

app = flask.Flask(__name__)
query = MovieQuery()

@app.route('/')
#Returns welcome msg when the users visits home route.
def hello():
	return "meow meow"

@app.errorhandler(404)
#Returns error msg when the page is not found.
def not_found_error_handler(e):
	return "Page not found."

@app.route('/topratedmovies/<int:first_n>')
#Returns a list of first n movies with top ratings.
def get_toprated(first_n):
	if first_n >= 0 and first_n < 10000:
		return query.get_toprated(first_n)
	return "Please enter a valid url for toprated movies query."

@app.route('/<int:year>/toppicks/<int:first_n>')
#Returns a list of first n movies with top ratings in a given year.
def get_favourite_from_year(year, first_n):
	if year >= 1970 and year <= 2016 and first_n >= 0 and first_n < 10000:
		return query.get_favourite_from_year(year, first_n)
	return "Please enter a valid url for get favourite movies from year query."

@app.route('/recentrelease/<int:first_n>')
#Returns a list of first n movies in recent release.
def get_recent_release(first_n):
	if first_n >= 0 and first_n < 10000:
		return query.get_recent_release(first_n)
	return "Please enter a valid url for recent release query."

@app.route('/<genre>/<int:first_n>')
#Returns a list of first n movies with top ratings in a given genre.
def get_toprated_in_genre(genre, first_n):
	genre = genre.lower()
	genre_set = set(['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir', 'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action', 'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax'])
	if first_n >= 0 and first_n < 10000 and (genre in genre_set):
		return query.get_toprated_in_genre(genre, first_n)
	return "Please enter a valid url for get toprated in genre query."

@app.route('/titlecontains')
#Returns a list of movies whose title contain the given string.
def get_movies_containing_title():
	string = request.args.get("query")
	return query.get_movies_containing_title(string)

if __name__ == '__main__':
	app.debug = True
	#app.run(host='thacker.mathcs.carleton.edu', port=5128)
	app.run(host='localhost', port=8888)
