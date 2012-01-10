from flask import session,g
import models
import datetime
from pprint import pprint

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
	txns = slice_txns(txns,t_id)
	txns = [get_txn_obj(txn) for txn in txns]
	txns = [process_txn(txn) for txn in txns]

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
		raise

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

def process_txn(txn):
	ac_nos = g.user.get_account_nos()
	if txn.method == 'XFER':
		if txn.t_type == 'c' and txn.party in ac_nos:
			txn.t_type = 'x'

		if txn.t_type == 'd' and txn.party in ac_nos:
			txn.t_type = 'x'
	pprint(txn.response())
	return txn
