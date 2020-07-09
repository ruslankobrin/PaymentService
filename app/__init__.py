import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config.from_object('app.config')

from payment.views import payment

app.register_blueprint(payment)

bootstrap = Bootstrap(app)

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
formatter = \
    logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)