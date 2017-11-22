from wtforms import validators
from wtforms.fields import StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm


class ContactForm(FlaskForm):
    name = StringField(label='Имя',
                       validators=[validators.InputRequired()],
                       id='input-name',
                       render_kw={'placeholder': 'Ваше имя...'},
                       _name='name')
    email_addr = EmailField(validators=[validators.InputRequired(),
                                        validators.Email()],
                            id='input-email',
                            render_kw={'placeholder': 'Ваш Email...'},
                            _name='email_addr')
    message = TextAreaField(label='Сообщение',
                            validators=[validators.InputRequired()],
                            id='message-text',
                            render_kw={'placeholder': 'Ваше сообщение...',
                                       'rows': '5'},
                            _name='message')
