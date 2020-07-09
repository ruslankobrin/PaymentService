from flask_wtf import FlaskForm
from wtforms import FloatField, TextAreaField, SelectField, SubmitField
from wtforms.csrf.session import SessionCSRF
from wtforms.validators import NumberRange, InputRequired

from app.config import SECRET_KEY_CSRF
from payment.constants import CURRENCY_CHOICES


# class OrderForm(FlaskForm):
#     class Meta:
#         csrf = True
#         csrf_class = SessionCSRF
#         csrf_secret = SECRET_KEY_CSRF
#     amount = FloatField(
#         label='Сумма оплаты',
#         validators=[InputRequired(message='Это поле обязательно!'),
#                     NumberRange(min=1, message='Сумма оплаты должна быть больше 0!')]
#     )
#     currency = SelectField(
#         label='Валюта',
#         validators=[InputRequired(message='Это поле обязательно!')],
#         coerce=str,
#         choices=CURRENCY_CHOICES)
#     description = TextAreaField(label='Описание товара', validators=[InputRequired(message='Это поле обязательно!')])
#     submit_button = SubmitField('Оплатить')



from wtforms.csrf.session import SessionCSRF
from wtforms import Form
from wtforms import validators
from wtforms import SelectField, TextAreaField, StringField

class BaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = SECRET_KEY_CSRF


class RegistrationForm(BaseForm):
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
    description = TextAreaField(label='Описание товара', validators=[InputRequired(message='Это поле обязательно!')])
    submit_button = SubmitField('Оплатить')