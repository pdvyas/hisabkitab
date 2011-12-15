from flaskext.sqlalchemy import SQLAlchemy
import datetime
import flask
import hashlib
app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)
accounts = db.Table('accounts',
		    db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
			    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
				)

class User(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	#family_id = db.Column(db.Integer,db.ForeignKey('family.id'))
	name = db.Column(db.String(80),unique=True)
	password = db.Column(db.String(32))
	email = db.Column(db.String(80),unique=True)
	accounts = db.relationship('Account',secondary=accounts,
			backref=db.backref('users',lazy='dynamic'))

	def __init__(self,name,email,password):
		self.name = name
		self.email = email
		self.password = hashlib.md5(password).hexdigest()
	
	@staticmethod
	def auth(name,password):
		pwhash = hashlib.md5(password).hexdigest()
		usr = User.query.filter_by(name=name,password=pwhash).first()
		return usr

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

	def __init__(self,id,ref_no,narration,date,amount,t_type):
		self.id = id
		self.ref_no = ref_no
		self.narration = narration
		self.date = date
		self.amount = amount
		self.t_type = t_type
class Account(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	no = db.Column(db.String)
	bal = db.Column(db.Float)
	_last_txn = db.Column(db.String(32))
	transactions = db.relationship('Transaction',
			backref=db.backref('Transaction'),primaryjoin=id==Transaction.ac_id)
	def __init__(self,no):
		self.no = no

def test():
	db.drop_all()
	db.create_all()
	#family = Family('vyas')
	usr1 = User('pratik','pdvyas@gmail.com','secret')
	usr2= User('Neelima','neelu@gmail.com','secret2')
	#family.users.append(usr1)
	#family.users.append(usr2)
	ac1 = Account(810)
	ac2 = Account(940)
	usr1.accounts.append(ac2)
	usr2.accounts.append(ac1)
	usr2.accounts.append(ac2)
	t1 = Transaction('a','23','test',datetime.date(2011,11,23),100,'c')
	t2 = Transaction('b','232','tes2t',datetime.date(2010,11,23),200,'c')
	t3 = Transaction('c','2232','tes2t',datetime.date(2010,11,23),300,'d')
	ac1.transactions.append(t1)
	ac1.transactions.append(t2)
	ac2.transactions.append(t3)
	db.session.add(usr1)
	db.session.add(usr2)
	db.session.add(ac1)
	db.session.add(ac2)
	db.session.commit()
	print User.auth('pratik','secret').name
	print User.auth('pratik','asdf')

if __name__ == "__main__":
	test()

