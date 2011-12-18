from models import *
from flask import g,session
from app import app

@app.teardown_request
def teardown(e):
	db.session.close()

@app.before_request
def before_request():
	if 'user' in session:
		g.user = User.query.get(session['user'])
