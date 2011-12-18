from app import app
from flask import request,jsonify,session
import json
import datetime
import models
from bank import *

@app.route("/ext/account",methods=['POST'])
def get_acs():
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
