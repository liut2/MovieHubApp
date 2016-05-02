from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
from user_query import UserQuery
from api_query import MovieQuery
import json

SECRET_KEY = 'moviehub development key'
FACEBOOK_APP_ID = '260838524257280'
FACEBOOK_APP_SECRET = 'a0210b8252d9590f8bd7c1bbb645782c'

app = Flask(__name__)
app.secret_key = SECRET_KEY
oauth = OAuth()
userquery = UserQuery()
moviequery = MovieQuery()

facebook = oauth.remote_app('facebook',
	base_url='https://graph.facebook.com/',
	request_token_url=None,
	access_token_url='/oauth/access_token',
	authorize_url='https://www.facebook.com/dialog/oauth',
	consumer_key=FACEBOOK_APP_ID,
	consumer_secret=FACEBOOK_APP_SECRET,
	request_token_params={'scope': 'email'}
)

@app.route("/")
def index():
	genres = request.args.get('genres')
	movies = request.args.get('movies')
	genre_list = []
	toprated_in_genre = {}

	if genres != None:
		genres = json.loads(genres)
	
	if movies != None:
		movies = json.loads(movies)
	if genres != None and movies != None:
		session["alread_choose_preference"] = True
		userquery.update_user_preference(int(session["user_id"]), genres, movies)

	toprated = json.loads(moviequery.get_toprated(30))
	favourite_last_year = json.loads(moviequery.get_favourite_from_year(2015, 30))
	recent_release = json.loads(moviequery.get_recent_release(30))
	freq = [1, 2, 3, 4, 5]
	
	if "logged_in" in session and session["logged_in"]:
		user_obj = json.loads(userquery.find_user_by_id(int(session["user_id"])))
		genres = user_obj['selected_genres']
		movies = user_obj['selected_movies']
		for gen in genres:
			gen = gen.lower()
			toprated_in_genre["type"] = gen
			toprated_in_genre["body"] = json.loads(moviequery.get_toprated_in_genre(gen, 5))
			genre_list.append(toprated_in_genre)
			toprated_in_genre = {}
	print "finally here"
	print len(genre_list)
	return render_template("index.html", toprated = toprated, lastyear = favourite_last_year, recent = recent_release, freq = freq, genre_list = genre_list)

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

if __name__ == "__main__":
	app.run(debug=True)
