from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth
from user_query import UserQuery

SECRET_KEY = 'moviehub development key'
FACEBOOK_APP_ID = '260838524257280'
FACEBOOK_APP_SECRET = 'a0210b8252d9590f8bd7c1bbb645782c'

app = Flask(__name__)
app.secret_key = SECRET_KEY
oauth = OAuth()
userquery = UserQuery()

facebook = oauth.remote_app('facebook',
	base_url='https://graph.facebook.com/',
	request_token_url=None,
	access_token_url='/oauth/access_token',
	authorize_url='https://www.facebook.com/dialog/oauth',
	consumer_key=FACEBOOK_APP_ID,
	consumer_secret=FACEBOOK_APP_SECRET,
	request_token_params={'scope': 'email'}
)

@app.route("/", methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		session["alread_choose_preference"] = True
		print "post action"
		return redirect(url_for('login'))

	return render_template("index.html")


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
	#session["alread_signup"] = None

if __name__ == "__main__":
	app.run(debug=True)
