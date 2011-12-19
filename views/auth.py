from app import app
from flask import request,jsonify,session
from sqlalchemy.exc import IntegrityError
import models
@app.route("/")
def hello():
	raise Exception
	return jsonify({ 'a': 'Hello World!'})

@app.route("/register", methods=['POST'])
def register():
	name = request.form['name']
	email = request.form['email']
	password = request.form['password']
	usr = models.User(name,email,password)
	try:
		models.db.session.add(usr)
		models.db.session.commit()
	except IntegrityError,e:
		models.db.session.rollback()
		raise e
	return usr.response()

@app.route('/login',methods=['POST'])
def login():
	name = request.form['name']
	password = request.form['password']
	if not (name and password):
		return "bad bad"
	usr = models.User.auth(name,password)
	if usr:
		session['user'] = usr.id
		return "Logged in"
	else:
		return "Login Failed"

@app.route('/logout')
def logout():
	try:
		del session['user']
	except KeyError:
		pass
	return "Logged out"

@app.route('/user',methods=['GET'])
def test():
	try:
		user = models.User.query.get(session['user'])
		return user.response()
	except KeyError,e:
		return "Not Logged in"
