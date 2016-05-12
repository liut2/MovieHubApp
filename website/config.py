'''
	config.py
	Author : Tao Liu and Xi Chen.
	This file contains the variables setup for our web app.
'''

#variables for psql setup
database = "chenx2"
user = "chenx2"
password = "eye577recycle"
# database = "postgres"
# user = "postgres"
# password = "eye577recycle"

#variables for Facebook login setup
SECRET_KEY = 'moviehub development key'
FACEBOOK_APP_ID = '269409810070442'
FACEBOOK_APP_SECRET = 'd1d196dcf11ea97728d7b178535a6b9c'

#variables for rendering the page
LIMIT_PER_PAGE = 15

#variables for server setup
# host = "thacker.mathcs.carleton.edu"
# port = 5106
host = "local"
port = 5000