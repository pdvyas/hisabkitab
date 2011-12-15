from app import app
from flask import request,jsonify,session
import models
@app.route("/")
def hello():
	return jsonify({ 'a': 'Hello World!'})

@app.route('/login',methods=['GET'])
def login():
	name = request.args.get('name')
	password = request.args.get('password')
	if not (name and password):
		return "bad bad"
	usr = models.User.auth(name,password)
	if usr:
		session['user'] = usr
		return "Logged in"
	else:
		return "Login Failed"

@app.route('/logout')
def logout():
	if hasattr(session,'user'):
		del session['user']
	return "Logged out"

@app.route('/test')
def test():
	if hasattr(session,'user'):
		return session['user'].name
	else:
		return "Not Logged in"
