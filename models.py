from flaskext.sqlalchemy import SQLAlchemy
import datetime
import flask
import hashlib
import json
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)
accounts = db.Table('accounts',
		    db.Column('account_id', db.String(32), db.ForeignKey('account.id')),
			    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
				db.UniqueConstraint('account_id','user_id')
				)

class User(db.Model):
	__table_args__=(db.UniqueConstraint('name','email'),)
	#family_id = db.Column(db.Integer,db.ForeignKey('family.id'))
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(80))
	password = db.Column(db.String(32))
	email = db.Column(db.String(80))
	accounts = db.relationship('Account',secondary=accounts,
			backref=db.backref('users',lazy='dynamic'))

	def __init__(self,name,email,password):
		self.name = name
		self.email = email
		self.password = hashlib.md5(password).hexdigest()
	
	@staticmethod
	def get_by_id(uid):
		usr = User.query.filter_by(id=uid).first()
		return usr
	
	@staticmethod
	def auth(name,password):
		pwhash = hashlib.md5(password).hexdigest()
		usr = User.query.filter_by(name=name,password=pwhash).first()
		return usr

	@staticmethod
	def exists(name):
		if User.query.filter_by(name=name).first():
			return True
		else:
			return False
	
	def response(self):
		ret = {}
		ret['id'] =	self.id
		ret['name'] = self.name
		return json.dumps(ret)
	
class Family(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(80))
	# users = db.relationship('User',
	#		backref=db.backref('user'),primaryjoin=id==User.family_id)

	def __init__(self,name):
		self.name = name
	


class Transaction(db.Model):
	id = db.Column(db.String(32),primary_key=True)
	ac_id = db.Column(db.Integer,db.ForeignKey('account.id'))
	ref_no = db.Column(db.String(80))
	narration = db.Column(db.String(80))
	date = db.Column(db.DateTime())
	amount = db.Column(db.Float(80))
	t_type = db.Column(db.String(1))
	bal = db.Column(db.Float)
	method = db.Column(db.String(10))
	card = db.Column(db.String(80))
	place = db.Column(db.String(80))
	party = db.Column(db.String(80))

	def __init__(self,id,ref_no,narration,date,amount,t_type,bal,method,card,place,party):
		self.id = id
		self.ref_no = ref_no
		self.narration = narration
		self.date = date
		self.amount = amount
		self.method = method
		self.bal = bal
		self.t_type = t_type
		self.card = card
		self.place = place
		self.party = party
	
	def response(self,as_dict=False):
		ret = { i : self.__getattribute__(i) for i in
				['id','ref_no','narration','date','amount','t_type','bal','ac_id','place','party','card','method']}
		ret['date']=ret['date'].isoformat()
		if as_dict:
			return ret
		return json.dumps(ret)

	@staticmethod
	def get_by_id(t_id):
		return Transaction.query.get(t_id)

class Account(db.Model):
	id = db.Column(db.String, primary_key=True)
	no = db.Column(db.String)
	bank = db.Column(db.String)
	bal = db.Column(db.Float)
	_last_txn = db.Column(db.String(32))
	_last_date = db.Column(db.DateTime())
	transactions = db.relationship('Transaction',
			backref=db.backref('Transaction'),primaryjoin=id==Transaction.ac_id)
	def __init__(self,ac_no,bank,id,balance):
		self.id = id
		self.bal = balance
		self.no = ac_no
		self.bank = bank

	@staticmethod
	def get_by_id(ac_id):
		return Account.query.get(ac_id)

	def response(self,as_dict=False):
		ret = { i : self.__getattribute__(i) for i in
				['id','no','bank','bal']}
		if as_dict:
			return ret
		return json.dumps(ret)
