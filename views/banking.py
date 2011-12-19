from app import app
from flask import request,jsonify,session,g
import json
import datetime
import models
from bank import *

@app.route("/account",methods=['GET'])
def get_acs():
	user = g.user
	accounts = user.accounts
	accounts = [ac.response(as_dict=True) for ac in accounts]
	return json.dumps(accounts)

@app.route("/account/<acid>",methods=['GET'])
def get_ac(acid):
	user = g.user
	account = models.Account.get_by_id(acid)
	if account in user.accounts:
		return account.response()
	else:
		return "account not found"

@app.route("/ext/account",methods=['POST'])
def get_ext_acs():
	bankname = request.form['bank']
	username = request.form['username']
	password = request.form['password']
	acs = get_accounts(bankname,username,password)
	session['LOA'] = { i['id'] : i for i in acs}
	ret = json.dumps(acs)
	return ret

@app.route("/account/auth",methods=['POST'])
def auth_ac():
	ac_id = request.form['ac_id']
	user = g.user
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

@app.route("/account/<acid>/transaction")
def get_txns(acid):
	txns = []
	user = g.user
	account = models.Account.get_by_id(acid)
	if account in user.accounts:
		txns = account.transactions
		txns = [txn.response(as_dict=True) for txn in txns]
	return json.dumps(txns)

@app.route("/transaction/<tid>")
def get_txn(tid):
	user = g.user
	txn = models.Transaction.get_by_id(tid)
	account = models.Account.get_by_id(txn.ac_id)
	if account in user.accounts:
		return txn.response()
	return ""
