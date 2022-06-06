from flask_security.forms import Form, StringField, validators, Email, PasswordField, BooleanField, SubmitField
from wtforms import SelectMultipleField, IntegerField, SelectField
from wtforms.validators import EqualTo, ValidationError

from app.models import User


class SearchForm(Form):
    search = StringField(label="Введите искомого пользователя")

def get_obj_edit_profile_form(user, access_roles = None):
    class EditProfileForm(Form):
        username = StringField(label="Username")
        first_name = StringField("Имя", validators=[validators.DataRequired()])
        last_name = StringField("Фамилия", validators=[validators.DataRequired()])
        email = StringField("Email", validators=[validators.DataRequired(), Email()])

        def __init__(self, original_username, original_email, *args, **kwargs):
            super(EditProfileForm, self).__init__(*args, **kwargs)
            self.original_username = original_username
            self.original_email = original_email

        def validate_email(self, email):
            # Если емаил в форме остался таким же (не поменяли), то не проверяем его на корректность
            if email.data != self.original_email:
                user = User.query.filter_by(email=email.data).first()
                if user is not None:
                    raise ValidationError("Этот email уже зарегистрирован. Попробуйте восстановить пароль")

        def validate_username(self, username):
            if username.data != self.original_username:
                user = User.query.filter_by(username=username.data).first()
                if user is not None:
                    raise ValidationError("Этот username уже зарегистрирован. Попробуйте восстановить пароль")


    roles = SelectMultipleField("Роли", coerce=int, choices=[(role.id, role.name) for role in access_roles],
                                default=[role.id for role in user.roles])

    setattr(EditProfileForm, "roles", roles)
    submit = SubmitField("Изменить")
    setattr(EditProfileForm, "submit", submit)

    return EditProfileForm(user.username, user.email)

class ResetPasswordForm(Form):
    current_password = PasswordField("Текущий пароль", validators=[validators.DataRequired()])
    password = PasswordField("Новый пароль", validators=[validators.DataRequired()])
    password_repeat = PasswordField("Повторите новый пароль", validators=[validators.DataRequired(), EqualTo("password")])
    submit = SubmitField("Изменить")


class EditStudentDataForm(Form):
    sure_name = StringField("Введите Ваше отчество", validators=[validators.DataRequired()])
    theme_NKR = StringField("Введите тему НКР", validators=[validators.DataRequired()])
    supervisor = StringField("Введите Вашего руководителя", validators=[validators.DataRequired()])
    NK_pages = IntegerField("Введите НД страниц", validators=[validators.NumberRange(min=1)])
    NKR_pages = IntegerField("Введите НКР страниц", validators=[validators.NumberRange(min=1)])
    slides_pages = IntegerField("Введите кол-во слайдов", validators=[validators.NumberRange(min=1)])
    group = IntegerField("Введите Вашу группу", validators=[validators.NumberRange(min=1)])
    specialize = StringField("Введите Вашу специальность", validators=[validators.DataRequired()])
    type_education = SelectField("Выберите тип обучения", default="очное", choices=["очное", "заочное"])
    department = SelectField("Введите Ваш факультет", choices=["ФКТИ", "ФРТ", "ФЭЛ"])
    submit = SubmitField("Отправить")