from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
from user_query import UserQuery
from api_query import MovieQuery
import json
import random

SECRET_KEY = 'moviehub development key'
FACEBOOK_APP_ID = '260838524257280'
FACEBOOK_APP_SECRET = 'a0210b8252d9590f8bd7c1bbb645782c'

app = Flask(__name__)
app.secret_key = SECRET_KEY
oauth = OAuth()
userquery = UserQuery()
moviequery = MovieQuery()
LIMIT_PER_PAGE = 15

facebook = oauth.remote_app('facebook',
	base_url='https://graph.facebook.com/',
	request_token_url=None,
	access_token_url='/oauth/access_token',
	authorize_url='https://www.facebook.com/dialog/oauth',
	consumer_key=FACEBOOK_APP_ID,
	consumer_secret=FACEBOOK_APP_SECRET,
	request_token_params={'scope': 'email'}
)

genre_list = []

@app.route("/",methods=['POST', 'GET'])
def index():
	global genre_list
	
	if request.method == "POST":
		response = request.json
		session["alread_choose_preference"] = True
		genres = response["selected_genres"]
		movies = response["selected_movies"]
		userquery.update_user_preference(int(session["user_id"]), genres, movies)
		toprated_in_genre = {}
		for gen in genres:
			gen = gen.lower()
			toprated_in_genre["type"] = gen
			toprated_in_genre["body"] = json.loads(moviequery.get_toprated_in_genre(gen, 30))
			genre_list.append(toprated_in_genre)
			toprated_in_genre = {}

		return "success"

	toprated = json.loads(moviequery.get_toprated(30))
	favourite_last_year = json.loads(moviequery.get_favourite_from_year(2015, 30))
	recent_release = json.loads(moviequery.get_recent_release(30))
	freq = [1, 2, 3, 4, 5]
	
	#used for genre preference list
	genre_preference = ['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir', 'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action', 'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax']
	#used for movie preference list
	movie_preference = []
	movie_set = set()
	for gen in genre_preference:
		rows = json.loads(moviequery.get_toprated_in_genre(gen, 4))
		for i in range(len(rows)):
			title = rows[i]["title"]
			if len(title) < 20 and (title not in movie_set):
				movie_preference.append(rows[i])
				movie_set.add(title)
	#randomize the order
	genre_preference = shuffle(genre_preference)
	movie_preference =  shuffle(movie_preference)
	
	return render_template("index.html", toprated = toprated, lastyear = favourite_last_year, recent = recent_release, freq = freq, genre_list = genre_list, genre_preference = genre_preference, movie_preference = movie_preference)

@app.route("/search")
def search():
	string = request.args.get("query").lower()
	search_result = json.loads(moviequery.get_movies_containing_title(string))
	return render_template("search_page.html",word=string,search_result = search_result, total_page_count= 1)

@app.route("/<type>")
def seemore(type):
	nth_page = int(request.args.get("page"))
	if type == "toprated":
		toprated = json.loads(moviequery.get_toprated_with_pagination(LIMIT_PER_PAGE, nth_page))
		total_page_count = moviequery.get_toprated_with_page_count(LIMIT_PER_PAGE)
		return render_template("search_page.html",word="Top Rated", search_result = toprated, total_page_count = total_page_count)

	elif type == "recentrelease":
		recentrelease = json.loads(moviequery.get_favourite_from_year_with_pagination(2016, LIMIT_PER_PAGE, nth_page))
		total_page_count = moviequery.get_favourite_from_year_with_page_count(2016, LIMIT_PER_PAGE)
		return render_template("search_page.html",word="Recent release", search_result = recentrelease, total_page_count = total_page_count)

	elif type == "favoritefromlastyear":
		favoritefromlastyear = json.loads(moviequery.get_favourite_from_year_with_pagination(2015, LIMIT_PER_PAGE, nth_page))
		total_page_count = moviequery.get_favourite_from_year_with_page_count(2015, LIMIT_PER_PAGE)
		return render_template("search_page.html",word="Favorite from Last Year", search_result = favoritefromlastyear, total_page_count = total_page_count)

	else:
		#genre_set = set(['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir', 'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action', 'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax'])
		genre = json.loads(moviequery.get_toprated_in_genre_with_pagination(type.lower(), LIMIT_PER_PAGE, nth_page))
		total_page_count = moviequery.get_toprated_in_genre_with_page_count(type.lower(), LIMIT_PER_PAGE)
		return render_template("search_page.html",word=type.title(), search_result = genre, total_page_count = total_page_count)
	

@app.route('/login')
def login():
	return facebook.authorize(callback=url_for('facebook_authorized',
		next=request.args.get('next') or request.referrer or None,
		_external=True))

@app.route("/logout")
def logout():
	pop_login_session()
	return redirect(url_for('index'))

@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
	if resp is None:
		return redirect(url_for('index'))

	session['oauth_token'] = (resp['access_token'], '')
	session['logged_in'] = True


	me = facebook.get('/me')
	user_id = int(me.data['id'])
	user_name = me.data['name']
	session['user_id'] = user_id
	session['user_name'] = user_name

	if userquery.check_if_user_exist(user_id):
		session["alread_choose_preference"] = True
		print "alread_signup"
	else:
		userquery.add_user(user_id, user_name)
		session["alread_choose_preference"] = False
		print "not_signup"
	
	return redirect(url_for('index'))

@facebook.tokengetter
def get_facebook_token():
	return session.get('oauth_token')

def pop_login_session():
	session.pop('logged_in', None)
	session.pop('oauth_token', None)
	session.pop('user_id', None)
	session.pop('user_name', None)
	#session["alread_signup"] = None

def shuffle(arr):
	for i in range(len(arr)):
		r = random.randrange(len(arr))
		temp = arr[i]
		arr[i] = arr[r]
		arr[r] = temp
	return arr

if __name__ == "__main__":
	app.run(debug=True, host="localhost", port=5000)
