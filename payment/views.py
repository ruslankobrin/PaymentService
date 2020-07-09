import uuid

from flask import Blueprint, render_template, request, session

from app import app
from payment.forms import PaymentForm
from payment.services import get_piastrix_service, get_piastrix_action

payment = Blueprint(name='payment', import_name=__name__, template_folder='templates')



@payment.route('/', methods=('GET', 'POST'))
def index():
    form = PaymentForm(request.form, meta={'csrf_context': session})
    if request.method == 'POST' and form.validate():
        amount = form.amount.data
        currency = form.currency.data
        description = form.description.data
        id = str(uuid.uuid1())
        app.logger.info(
            f'The order form requested with data: id:{id} amount:{amount} currency:{currency} description:{description}')
        piastrix = get_piastrix_service(amount, currency, description, id)
        try:
            return get_piastrix_action(piastrix, currency)
        except (Exception) as e:
            app.logger.error('Error during piastrix action - {}'.format(e))
    return render_template('main.html', form=form)