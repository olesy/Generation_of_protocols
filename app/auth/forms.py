from flask_security.forms import Form, StringField, validators, Email, PasswordField, BooleanField, SubmitField
from wtforms.validators import EqualTo, ValidationError

from app.models import User


class LoginForm(Form):
    #validators - чтобы при нажатии на кнопку отправить данные отправились на сервер, DataRequired() - поле обяз к заполнени
    #Email() - на соответствие емайлу
    email = StringField("Email", validators=[validators.DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[validators.DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")

class RegistrationForm(Form):
    username = StringField("Username", validators=[validators.DataRequired()])
    first_name = StringField("Имя", validators=[validators.DataRequired()])
    last_name = StringField("Фамилия", validators=[validators.DataRequired()])
    email = StringField("Email", validators=[validators.DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[validators.DataRequired()])
    password_repeat = PasswordField("Повторите пароль", validators=[validators.DataRequired(), EqualTo("password")])
    submit = SubmitField("Зарегистрироваться")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError("Этот email уже зарегистрирован. Попробуйте восстановить пароль")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("Этот username уже зарегистрирован. Попробуйте восстановить пароль")
