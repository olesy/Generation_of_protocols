import os

from flask_security.utils import hash_password

from app import create_app, db, user_data_store
from app import models
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = create_app()
@app.shell_context_processor
def make_shell_context():
    return {
        "db" : db,
        "User" : models.User,
        "Role" : models.Role,
        "user_roles" : models.user_roles,
        "user_data_store" : user_data_store,
        "student_data" : models.StudentData
    }
# Запускается в момент запуска сервера
@app.before_first_request
def first_init():
    if not models.Role.query.get(1):
        student_role = models.Role(id = 1, name = "student")
        db.session.add(student_role)
        db.session.commit()
    if not models.Role.query.get(2):
        tutor_role = models.Role(id = 2, name = "tutor")
        db.session.add(tutor_role)
        db.session.commit()
    if not models.User.query.get(1):
        u = user_data_store.create_user(id = 1, username = "Olesya", email="dub-4317@yandex.ru",
                                        first_name="Olesya",
                                        last_name="Ivleva",
                                        password=hash_password("nhuJu3"))
        db.session.add(u)
        db.session.commit()
        r = models.Role.query.get(2)
        u = models.User.query.get(1)
        u.roles.append(r)
        db.session.add(u)
        db.session.commit()



