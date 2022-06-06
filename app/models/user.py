from datetime import datetime

from flask_security import UserMixin

from app import db, login
from app.models.user_role import user_roles


class User(UserMixin, db.Model):
    # Задает название таблицы в бд
    __tablename__ = "users"
    __comment__ = "Пользователи"
    # primary_key - первичный ключ. Дуюликаты невозможны (не могут быть одинаков идентификаторы)
    id = db.Column(db.Integer, primary_key=True, comment="id user")
    # index - бд ищет по индексированным занчениям (для быстроты поиска), unique - не может быть два одинак. польз
    # nullable - обяз к заполнен
    # backref - под каким именем можно будет получить данные юзера
    username = db.Column(db.Text, index=True, unique=True, nullable=False)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, index=True, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean)
    # КОгда подтвердилась почта
    confirmed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    #backref - как получаем из таблицы юзеров, secondary - промежуточная таблица для связи с классом User
    # roles = db.relationship("Role", secondary=user_roles, backref = "users", lazy="dynamic")
    roles = db.relationship("Role", secondary=user_roles, backref="users")
    student_data = db.relationship("StudentData", backref="u", uselist=False)

    def __repr__(self):
        return f"<User {self.username}>"

    def has_role(self, *args):
        return set(args).issubset({role.name for role in self.roles})

#Механизм сессий, по какому правилу достаем пользователя. Этот человек был авторихован и не обяз при переходе на нов страницу
#вводить логин и пароль
@login.user_loader
def load_user(user_id):
    #orm_sql_alchemy. Из польз хотим исп запрос, по id выйти на запись в бд
    return User.query.get(int(user_id))

