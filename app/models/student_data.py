from flask_security import UserMixin

from app import db
from app.models.user_role import user_roles


class StudentData(UserMixin, db.Model):
    # Задает название таблицы в бд
    __tablename__ = "student_data"
    __comment__ = "Данные студентов"
    # primary_key - первичный ключ. Дуюликаты невозможны (не могут быть одинаков идентификаторы)
    id = db.Column(db.Integer, primary_key=True)
    # index - бд ищет по индексированным занчениям (для быстроты поиска), unique - не может быть два одинак. польз
    # nullable - обяз к заполнен
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    sure_name = db.Column(db.Text, nullable=False)
    theme_NKR = db.Column(db.Text, nullable=False)
    supervisor = db.Column(db.Text, nullable=False)
    NK_pages = db.Column(db.Integer, nullable=False)
    NKR_pages = db.Column(db.Integer, nullable=False)
    slides_pages = db.Column(db.Integer, nullable=False)
    group = db.Column(db.Integer, nullable=False)
    specialize = db.Column(db.Text, nullable=False)
    type_education = db.Column(db.Text, nullable=False)
    department = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<User {self.user_id}>"