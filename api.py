from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
from user_query import UserQuery
from api_query import MovieQuery
from recommender import Recommender
import json
import random
import config
from pagination import Pagination

'''
	app.py
	author: Tao Liu and Xi Chen
	Controller that handles rendering pages for our web app
'''

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
recommender = Recommender()
LIMIT_PER_PAGE = config.LIMIT_PER_PAGE
genre_list = []
movie_list = []
movie_preference = []
genre_preference = []
all_genre = ['mystery', 'romance', 'sci-fi', 'horror', 'children', 'film-noir', 'crime', 'drama', 'fantasy', 'animation', 'adventure', 'western', 'action', 'musical', 'comedy', 'documentary', 'war', 'thriller', 'imax']

'''This controller handles root route and renders home page for our web app.'''
@app.route("/",methods=['POST', 'GET'])
def index():
	global genre_list
	global movie_list
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
	recent_release = json.loads(moviequery.get_recent_release_for_page(1,30))
	locked_content_count = [1, 2, 3, 4, 5]
	init_preference_chosen_list()
	
	return render_template("index.html", toprated = toprated, lastyear = favourite_last_year, recent = recent_release, freq = locked_content_count, genre_list = genre_list, movie_list = movie_list, genre_preference = genre_preference, movie_preference = movie_preference)

'''This controller handles the route for rendering details for a specific movie channel.'''
@app.route("/<type>")
def seemore(type):
	result_empty = True
	if (request.args.get("page") is None):
		page = 1
	else:
		page = request.args.get("page")
		if(page.isdigit()):
			page = int(request.args.get("page"))
		else:
			return render_template('404.html'), 404
			
	if type == "search":
		string = request.args.get("query").lower()
		count = moviequery.get_movies_containing_title_with_count(string)
		search_result = json.loads(moviequery.get_movies_containing_title_for_page(string, page, LIMIT_PER_PAGE))
		pagination = Pagination(page, LIMIT_PER_PAGE, count)
		if(not search_result):
			result_empty = False
			return render_template("search_page.html",type = "search",word=string+" not found",search_result = search_result,pagination = pagination,result_empty = result_empty)
		else:
			return render_template("search_page.html",type = "search",word=string,search_result = search_result,pagination = pagination,result_empty = result_empty)

	if type == "toprated":
		toprated = json.loads(moviequery.get_toprated_for_page(page, LIMIT_PER_PAGE))
		count = moviequery.get_toprated_with_count()
		if (not check_page_valid(page,count)):
			return render_template('404.html'), 404
		pagination = Pagination(page, LIMIT_PER_PAGE, count)
		return render_template("search_page.html",type = type,word="Top Rated",search_result = toprated, pagination = pagination,result_empty = result_empty)

	elif type == "recentrelease":
		recentrelease = json.loads(moviequery.get_favourite_from_year_for_page(2016, page, LIMIT_PER_PAGE))
		count = moviequery.get_favourite_from_year_with_count(2016)
		if (not check_page_valid(page,count)):
			return render_template('404.html'), 404
		pagination = Pagination(page, LIMIT_PER_PAGE, count)
		return render_template("search_page.html",type = type,word="Recent Release",search_result = recentrelease, pagination = pagination,result_empty = result_empty)

	elif type == "favoritefromlastyear":
		favoritefromlastyear = json.loads(moviequery.get_favourite_from_year_for_page(2015, page, LIMIT_PER_PAGE))
		count = moviequery.get_favourite_from_year_with_count(2015)
		if (not check_page_valid(page,count)):
			return render_template('404.html'), 404
		pagination = Pagination(page, LIMIT_PER_PAGE, count)
		return render_template("search_page.html",type = type,word="Favorite From Last Year",search_result = favoritefromlastyear, pagination = pagination,result_empty = result_empty)

	elif type in all_genre:
		genre = json.loads(moviequery.get_toprated_in_genre_for_page(type.lower(), page, LIMIT_PER_PAGE))
		count = moviequery.get_toprated_in_genre_with_count(type.lower())
		if (not check_page_valid(page,count)):
			return render_template('404.html'), 404
		pagination = Pagination(page, LIMIT_PER_PAGE, count)
		return render_template("search_page.html",type = type,word=type,search_result = genre, pagination = pagination,result_empty = result_empty)

	elif type == "customizedmoviesforyou":
		customizedmoviesforyou = movie_list
		count = len(customizedmoviesforyou)
		if (not check_page_valid(page,count)):
			return render_template('404.html'), 404
		pagination = Pagination(page, LIMIT_PER_PAGE, count)
		customizedmoviesforyou = customizedmoviesforyou[(page-1)*LIMIT_PER_PAGE:page*LIMIT_PER_PAGE]
		return render_template("search_page.html",type = type,word="Customized Movies for You",search_result = customizedmoviesforyou, pagination = pagination,result_empty = result_empty)

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

def check_page_valid(page,count):
	remainer = count % LIMIT_PER_PAGE
	if(remainer != 0):
		if (count / LIMIT_PER_PAGE + 1 < page):
			return False
	else:
		if (count / LIMIT_PER_PAGE < page):
			return False
	return True

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
	global movie_list
	toprated_in_genre = {}
	for gen in genres:
		gen = gen.lower()
		toprated_in_genre["type"] = gen
		toprated_in_genre["body"] = json.loads(moviequery.get_toprated_in_genre_for_page(gen, 1,30))
		genre_list.append(toprated_in_genre)
		toprated_in_genre = {}
	print("update user preference")
	recommended_list = recommender.find_movie_for_you(movies, 3)
	movie_list = json.loads(moviequery.get_movies_by_id(recommended_list))


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


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port = config.port)
