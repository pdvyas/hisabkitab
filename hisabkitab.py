from app import app
import logging
from views import *
file_handler = logging.FileHandler('log.log')
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)
app.secret_key = '12343'
if __name__ == "__main__":
    app.run('0.0.0.0',debug=True)
