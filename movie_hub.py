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

#in unit test, we need to check first_n is a valid number
@app.route('/topratedmovies/<int:first_n>')
def get_toprated(first_n):
    if first_n <=0 or first_n > 10000:
        return "please enter a valid number"
    return query.get_toprated(first_n)
    
@app.route('/<int:year>/toppicks/<int:first_n>')
def get_favourite_from_year(year, first_n):
    if year < 1970 or year > 2016:
        return "please enter a valid year"
    if first_n <=0 or first_n > 10000:
        return "please enter a valid number"
    return query.get_favourite_from_year(year, first_n)
    
@app.route('/recentrelease/<int:first_n>')
def get_recent_release(first_n):
    if first_n <=0 or first_n > 10000:
        return "please enter a valid number"
    return query.get_recent_release(first_n)

#we also need to check if the imput genre is in the genre list
#this also need to be tested in unittest
@app.route('/<genre>/<int:first_n>')
def get_toprated_in_genre(genre, first_n):
    if first_n <=0 or first_n > 10000:
        return "please enter a valid number"
    return query.get_toprated_in_genre(genre, first_n)

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