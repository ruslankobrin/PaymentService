from wtforms import FloatField, TextAreaField, SelectField, SubmitField
from wtforms.csrf.session import SessionCSRF
from wtforms.validators import NumberRange, InputRequired
from wtforms import Form

from app.config import SECRET_KEY_CSRF
from payment.constants import CURRENCY_CHOICES


class PaymentForm(Form):

    amount = FloatField(
        label='Сумма оплаты',
        validators=[InputRequired(message='Это поле обязательно!'),
                    NumberRange(min=1, message='Сумма оплаты должна быть больше 0!')]
    )

    currency = SelectField(
        label='Валюта',
        validators=[InputRequired(message='Это поле обязательно!')],
        coerce=str,
        choices=CURRENCY_CHOICES)

    description = TextAreaField(
        label='Описание товара',
        validators=[InputRequired(message='Это поле обязательно!')])

    submit_button = SubmitField('Оплатить')

    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = SECRET_KEY_CSRF