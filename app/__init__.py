from flask import Flask

app = Flask(__name__)

app.config.from_object('app.config')

from payment.views import payment

app.register_blueprint(payment)