from flask import Flask, redirect, url_for, session, request, render_template
from flask_oauth import OAuth

SECRET_KEY = 'moviehub development key'
FACEBOOK_APP_ID = '260838524257280'
FACEBOOK_APP_SECRET = 'a0210b8252d9590f8bd7c1bbb645782c'

app = Flask(__name__)
app.secret_key = SECRET_KEY
oauth = OAuth()

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
    print 'Logged in as id=%s name=%s'  % \
        (me.data['id'], me.data['name'])
    return redirect(url_for('index'))

@facebook.tokengetter
def get_facebook_token():
    return session.get('oauth_token')

def pop_login_session():
    session.pop('logged_in', None)
    session.pop('oauth_token', None)

if __name__ == "__main__":
    app.run(debug=True)
