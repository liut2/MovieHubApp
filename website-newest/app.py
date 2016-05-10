from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
from user_query import UserQuery
from api_query import MovieQuery
import json
import random
import config
from Pagination import Pagination

app = Flask(__name__)

#import Facebook login setup from config.py
SECRET_KEY = config.SECRET_KEY
FACEBOOK_APP_ID = config.FACEBOOK_APP_ID
FACEBOOK_APP_SECRET = config.FACEBOOK_APP_SECRET
app.secret_key = SECRET_KEY
oauth = OAuth()

#init Facebook login setup
facebook = oauth.remote_app('facebook',
	base_url='https://graph.facebook.com/',
	request_token_url=None,
	access_token_url='/oauth/access_token',
	authorize_url='https://www.facebook.com/dialog/oauth',
	consumer_key=FACEBOOK_APP_ID,
	consumer_secret=FACEBOOK_APP_SECRET,
	request_token_params={'scope': 'email'}
)

#declaration of other variables
userquery = UserQuery()
moviequery = MovieQuery()
LIMIT_PER_PAGE = config.LIMIT_PER_PAGE
genre_list = []
movie_preference = []
genre_preference = []
all_genre = ['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir', 'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action', 'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax']


'''This controller handles root route and renders home page for our web app.'''
@app.route("/",methods=['POST', 'GET'])
def index():
	global genre_list
	# Receiving Ajax POST request means user has updated their preference, then we update the info 
	# in database and reload our page to show that update.
	if request.method == "POST":
		response = request.json
		session["alread_choose_preference"] = True
		genres = response["selected_genres"]
		movies = response["selected_movies"]
		update_user_preference(genres, movies)
		return "success"

	#else if the request is GET, we simply render the template as we normally do.
	toprated = json.loads(moviequery.get_toprated_for_page(1,30))
	favourite_last_year = json.loads(moviequery.get_favourite_from_year_for_page(2015, 1,30))
	recent_release = json.loads(moviequery.get_favourite_from_year_for_page(2016,1,30))
	locked_content_count = [1, 2, 3, 4, 5]
	init_preference_chosen_list()
	
	return render_template("index.html", toprated = toprated, lastyear = favourite_last_year, recent = recent_release, freq = locked_content_count, genre_list = genre_list, genre_preference = genre_preference, movie_preference = movie_preference)

'''This controller handles the route for search page, and renders the search results.'''
@app.route("/search")
def search():
	result_empty = True
	string = request.args.get("query").lower()
	search_result = json.loads(moviequery.get_movies_containing_title(string))
	pagination = Pagination(1, LIMIT_PER_PAGE, 1)
	if(not search_result):
		result_empty = False
		return render_template("search_page.html",type = "search",word=string+" not found",search_result = search_result,pagination = pagination,result_empty = result_empty)
	else:
		return render_template("search_page.html",type = "search",word=string,search_result = search_result,pagination = pagination,result_empty = result_empty)

'''This controller handles the route for rendering details for a specific movie channel.'''
@app.route("/<type>",defaults={'page': 1})
@app.route("/<type>/page/<int:page>")
def seemore(type,page):
	result_empty = True
	if type == "toprated":
		toprated = json.loads(moviequery.get_toprated_for_page(page, LIMIT_PER_PAGE))
		count = moviequery.get_toprated_with_count()
		pagination = Pagination(page, LIMIT_PER_PAGE, count)
		return render_template("search_page.html",type = type,word="Top Rated",search_result = toprated, pagination = pagination,result_empty = result_empty)
	elif type == "recentrelease":
		recentrelease = json.loads(moviequery.get_favourite_from_year_for_page(2016, page, LIMIT_PER_PAGE))
		count = moviequery.get_favourite_from_year_with_count(2016)
		pagination = Pagination(page, LIMIT_PER_PAGE, count)
		return render_template("search_page.html",type = type,word="Recent Release",search_result = recentrelease, pagination = pagination,result_empty = result_empty)
	elif type == "favoritefromlastyear":
		favoritefromlastyear = json.loads(moviequery.get_favourite_from_year_for_page(2015, page, LIMIT_PER_PAGE))
		count = moviequery.get_favourite_from_year_with_count(2015)
		pagination = Pagination(page, LIMIT_PER_PAGE, count)
		return render_template("search_page.html",type = type,word="Favorite From Last Year",search_result = favoritefromlastyear, pagination = pagination,result_empty = result_empty)
	elif type in all_genre:
		genre = json.loads(moviequery.get_toprated_in_genre_for_page(type.lower(), page, LIMIT_PER_PAGE))
		count = moviequery.get_toprated_in_genre_with_count(type.lower())
		pagination = Pagination(page, LIMIT_PER_PAGE, count)
		return render_template("search_page.html",type = type,word=type,search_result = genre, pagination = pagination,result_empty = result_empty)
	else:
		return render_template('404.html'), 404

'''This controller handles the route for login page, which redirects user
to Facebook login.'''
@app.route('/login')
def login():
	return facebook.authorize(callback=url_for('facebook_authorized',
		next=request.args.get('next') or request.referrer or None,
		_external=True))

'''This controller handles the route for logout page, which redirects user back to home page before login.'''
@app.route("/logout")
def logout():
	#clear user session when logout
	pop_login_session()
	return redirect(url_for('index'))

'''This controller handles the callback after user has successfully logged in with Facebook.'''
@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
	if resp is None:
		return redirect(url_for('index'))

	session['oauth_token'] = (resp['access_token'], '')
	session['logged_in'] = True

	#update user info in session
	me = facebook.get('/me')
	user_id = int(me.data['id'])
	user_name = me.data['name']
	session['user_id'] = user_id
	session['user_name'] = user_name

	if userquery.check_if_user_exist(user_id):
		session["alread_choose_preference"] = True
	else:
		userquery.add_user(user_id, user_name)
		session["alread_choose_preference"] = False
	
	return redirect(url_for('index'))

'''This section contains some helper methods that are used to construct 
functions above.'''

@facebook.tokengetter
def get_facebook_token():
	return session.get('oauth_token')

def pop_login_session():
	session.pop('logged_in', None)
	session.pop('oauth_token', None)
	session.pop('user_id', None)
	session.pop('user_name', None)

def shuffle(arr):
	for i in range(len(arr)):
		r = random.randrange(len(arr))
		temp = arr[i]
		arr[i] = arr[r]
		arr[r] = temp
	return arr

def update_user_preference(genres, movies):
	userquery.update_user_preference(int(session["user_id"]), genres, movies)
	global genre_list
	toprated_in_genre = {}
	for gen in genres:
		gen = gen.lower()
		toprated_in_genre["type"] = gen
		toprated_in_genre["body"] = json.loads(moviequery.get_toprated_in_genre_for_page(gen, 1,30))
		genre_list.append(toprated_in_genre)
		toprated_in_genre = {}

def init_preference_chosen_list():
	global genre_preference
	global movie_preference
	genre_preference = []
	movie_preference = []
	#generate genre preference list
	genre_preference = ['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir', 'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action', 'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax']
	#generate movie preference list
	movie_set = set()
	for gen in genre_preference:
		rows = json.loads(moviequery.get_toprated_in_genre_for_page(gen, 1,30))
		for i in range(len(rows)):
			title = rows[i]["title"]
			if len(title) < 20 and (title not in movie_set) and ("'" not in title):
				movie_preference.append(rows[i])
				movie_set.add(title)
	#randomize the order
	genre_preference = shuffle(genre_preference)
	movie_preference =  shuffle(movie_preference)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/api/v1.0/topratedmovies/<int:first_n>')
#Returns a list of first n movies with top ratings.
def get_toprated(first_n):
	if first_n >= 0 and first_n < 10000:
		return query.get_toprated_for_page(1,first_n)
	return "Please enter a valid url for toprated movies query."

@app.route('/api/v1.0/<int:year>/toppicks/<int:first_n>')
#Returns a list of first n movies with top ratings in a given year.
def get_favourite_from_year(year, first_n):
	if year >= 1970 and year <= 2016 and first_n >= 0 and first_n < 10000:
		return query.get_favourite_from_year_for_page(year, 1,first_n)
	return "Please enter a valid url for get favourite movies from year query."

@app.route('/api/v1.0/recentrelease/<int:first_n>')
#Returns a list of first n movies in recent release.
def get_recent_release(first_n):
	if first_n >= 0 and first_n < 10000:
		return query.get_favourite_from_year_for_page(2016,1,first_n)
	return "Please enter a valid url for recent release query."

@app.route('/api/v1.0/<genre>/<int:first_n>')
#Returns a list of first n movies with top ratings in a given genre.
def get_toprated_in_genre(genre, first_n):
	genre = genre.lower()
	genre_set = set(['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir', 'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action', 'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax'])
	if first_n >= 0 and first_n < 10000 and (genre in genre_set):
		return query.get_toprated_in_genre(genre, first_n)
	return "Please enter a valid url for get toprated in genre query."

@app.route('/api/v1.0/titlecontains')
#Returns a list of movies whose title contain the given string.
def get_movies_containing_title():
	string = request.args.get("query")
	return query.get_movies_containing_title(string)

if __name__ == "__main__":
	app.run(debug=True, host = config.host, port = config.port)
