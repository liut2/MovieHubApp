from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
from user_query import UserQuery
from api_query import MovieQuery
import json
import random
import config

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
	toprated = json.loads(moviequery.get_toprated(30))
	favourite_last_year = json.loads(moviequery.get_favourite_from_year(2015, 30))
	recent_release = json.loads(moviequery.get_recent_release(30))
	locked_content_count = [1, 2, 3, 4, 5]
	init_preference_chosen_list()
	
	return render_template("index.html", toprated = toprated, lastyear = favourite_last_year, recent = recent_release, freq = locked_content_count, genre_list = genre_list, genre_preference = genre_preference, movie_preference = movie_preference)

'''This controller handles the route for search page, and renders the search results.'''
@app.route("/search")
def search():
	string = request.args.get("query").lower()
	search_result = json.loads(moviequery.get_movies_containing_title(string))
	return render_template("search_page.html", word = string, search_result = search_result, total_page_count = 1)

'''This controller handles the route for rendering details for a specific movie channel.'''
@app.route("/<type>")
def seemore(type):
	nth_page = int(request.args.get("page"))
	if type == "toprated":
		toprated = json.loads(moviequery.get_toprated_with_pagination(LIMIT_PER_PAGE, nth_page))
		total_page_count = moviequery.get_toprated_with_page_count(LIMIT_PER_PAGE)
		return render_template("search_page.html",word = "Top Rated", search_result = toprated, total_page_count = total_page_count)

	elif type == "recentrelease":
		recentrelease = json.loads(moviequery.get_favourite_from_year_with_pagination(2016, LIMIT_PER_PAGE, nth_page))
		total_page_count = moviequery.get_favourite_from_year_with_page_count(2016, LIMIT_PER_PAGE)
		return render_template("search_page.html",word = "Recent release", search_result = recentrelease, total_page_count = total_page_count)

	elif type == "favoritefromlastyear":
		favoritefromlastyear = json.loads(moviequery.get_favourite_from_year_with_pagination(2015, LIMIT_PER_PAGE, nth_page))
		total_page_count = moviequery.get_favourite_from_year_with_page_count(2015, LIMIT_PER_PAGE)
		return render_template("search_page.html",word = "Favorite from Last Year", search_result = favoritefromlastyear, total_page_count = total_page_count)

	else:
		genre = json.loads(moviequery.get_toprated_in_genre_with_pagination(type.lower(), LIMIT_PER_PAGE, nth_page))
		total_page_count = moviequery.get_toprated_in_genre_with_page_count(type.lower(), LIMIT_PER_PAGE)
		return render_template("search_page.html",word = type.title(), search_result = genre, total_page_count = total_page_count)
	
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
		toprated_in_genre["body"] = json.loads(moviequery.get_toprated_in_genre(gen, 30))
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
		rows = json.loads(moviequery.get_toprated_in_genre(gen, 4))
		for i in range(len(rows)):
			title = rows[i]["title"]
			if len(title) < 20 and (title not in movie_set) and ("'" not in title):
				movie_preference.append(rows[i])
				movie_set.add(title)
	#randomize the order
	genre_preference = shuffle(genre_preference)
	movie_preference =  shuffle(movie_preference)


if __name__ == "__main__":
	app.run(debug=True, host = config.host, port = config.port)
