#!/usr/bin/env python3
import flask
import json
from flask import request
from query import Query

app = flask.Flask(__name__)
query = Query()

@app.route('/')
def hello():
    return "meow meow"
	

@app.errorhandler(404)
def not_found_error_handler(e):
	return "Page not found."

#in unit test, we need to check first_n is a valid number
@app.route('/topratedmovies/<int:first_n>')
def get_toprated(first_n):
    if first_n >= 0 and first_n < 10000:
		return query.get_toprated(first_n)
    return "Please enter a valid url for toprated movies query."
	

@app.route('/<int:year>/toppicks/<int:first_n>')
def get_favourite_from_year(year, first_n):
    if year >= 1970 and year <= 2016 and first_n >= 0 and first_n < 10000:
		return query.get_favourite_from_year(year, first_n)
    return "Please enter a valid url for get favourite movies from year query."
	

@app.route('/recentrelease/<int:first_n>')
def get_recent_release(first_n):
    if first_n >= 0 and first_n < 10000:
		return query.get_recent_release(first_n)
    return "Please enter a valid url for recent release query."
	

#we also need to check if the imput genre is in the genre list
#this also need to be tested in unittest
@app.route('/<genre>/<int:first_n>')
def get_toprated_in_genre(genre, first_n):
	genre = genre.lower()
	genre_set = set(['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir', 'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action', 'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax'])
	if first_n >= 0 and first_n < 10000 and (genre in genre_set):
		return query.get_toprated_in_genre(genre, first_n)
	return "Please enter a valid url for get toprated in genre query."
	
#here the query doesn't support multiple string like "the+star+war" yet,
#will add this functionality later, this also need to be tested in unittest
#also in flask the query paramter doesn't show up in url, we need to retrieve it
#from request.args, but the actual url in browser is /titlecontains?query=string
#in unit test, we need to check if the url is only /titlecontains, which means the string is None
@app.route('/titlecontains')
def get_movies_containing_title():
    string = request.args.get("query")
    return query.get_movies_containing_title(string)

if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)
