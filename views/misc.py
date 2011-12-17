from models import *
from app import app

@app.teardown_request
def teardown(e):
	db.session.close()
