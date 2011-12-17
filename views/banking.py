from app import app
from flask import request,jsonify,session
import json
import datetime
import models

@app.route("/ext/account",methods=['POST'])
def get_acs():
	bankname = request.form['bank']
	username = request.form['username']
	password = request.form['password']
	acs = get_accounts(bankname,username,password)
	session['LOA'] = { i['id'] : i for i in acs}
	ret = json.dumps(acs)
	print session['LOA']
	return ret

def get_accounts(bankname,username,password):
	bank = __import__('banks.'+bankname,globals={}, locals={},
			fromlist=['Bank'], level=-1)
	bank = bank.Bank(username)
	bank.start()
	try:
		bank.login(password)
		acs =  bank.get_accounts()
		bank.logout()
	except Exception,e:
		bank.logout()
		raise e
	return acs

@app.route("/account/auth",methods=['POST'])
def auth_ac():
	ac_id = request.form['ac_id']
	user = models.User.get_by_id(session['user'])
	account = models.Account.get_by_id(ac_id)
	if not account:
		ac = session['LOA'][ac_id]
		account = models.Account (**ac)
	del session['LOA']
	user.accounts.append(account)
	models.db.session.add(user)
	models.db.session.commit()
	return account.response()

@app.route("/account/sync",methods=['POST'])
def sync_ac():
	ac_id = request.form['ac_id']
	username = request.form['username']
	password = request.form['password']
	sync_account(ac_id,username,password)
	return "Success"
	
def sync_account(ac_id,username,password):
	"""
	Synchronize account with latest Transactions
	"""
	ac = models.Account.get_by_id(ac_id)
	to_date= datetime.date.today()
	t_id = None
	if ac._last_txn and ac._last_date:
		from_date = ac._last_date
		t_id = ac._last_txn
	else:
		from_date = to_date - datetime.timedelta(30)
	bankname = ac.bank
	ac_no = ac.no
	txns = get_statement(bankname,ac_id,ac_no,username,password,to_date,from_date)
	print 'txns is ',txns
	txns = slice_txns(txns,t_id)
	txns = [get_txn_obj(txn) for txn in txns]

	ac.transactions.extend(txns)
	if len(txns)>0:
		ac._last_txn = txns[0].id
		ac._last_date = txns[0].date
		ac.bal = txns[0].bal
	models.db.session.add(ac)
	models.db.session.commit()

def get_statement(bankname,ac_id,ac_no,username,password,to_date,from_date):
	"""
	Wrapper around Bank.get_account_statement
	"""
	bank = __import__('banks.'+bankname,globals={}, locals={},
			fromlist=['Bank'], level=-1)
	bank = bank.Bank(username)
	bank.start()
	try:
		bank.login(password)
		acs =  bank.get_accounts()
		acs  = [ i['id'] for i in acs]
		if not ac_id in acs:
			raise Exception,"Cannot update with this login"
		txns = bank.get_account_statement(ac_no,'x',from_date,to_date)
		bank.logout()
		return txns
	except Exception,e:
		bank.logout()
		raise e

def get_txn_obj(txn):
	"""
	get transaction object from dict
	"""
	kargs = dict((i,txn[i]) for i in txn.keys())
	del kargs['ac_id']
	return models.Transaction(**kargs)

def slice_txns(txns,t_id):
	"""
	get transactions only after t_id
	"""
	if t_id == None:
		return txns
	txn_list = []
	for txn in txns:
		if txn['id'] == t_id:
			break
		txn_list.append(txn)
	return txn_list
