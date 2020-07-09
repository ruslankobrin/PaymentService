from flask import Blueprint, render_template, request, session

from payment.forms import RegistrationForm

payment = Blueprint(name='payment', import_name=__name__, template_folder='templates')

@payment.route('/', methods=('GET', 'POST'))
def index():
    form = RegistrationForm(request.form, meta={'csrf_context': session})
    if request.method == 'POST' and form.validate():
        print(form.amount.data)
        print(form.currency.data)
        print(form.description.data)
        print(form.data.copy())
    return render_template('main.html', form=form)