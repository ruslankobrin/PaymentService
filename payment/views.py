from flask import Blueprint

payment = Blueprint(name='payment', import_name=__name__, template_folder='templates')

@payment.route('/')
def hello_world():
    return 'Hello World!'