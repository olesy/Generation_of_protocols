from flask_security import UserMixin
from app import db


class Role(UserMixin, db.Model):
    __tablename__ = "roles"
    #Так будут названы поля в бд
    # роли в main.py (создание)
    id = db.Column(db.Integer, primary_key=True, comment="id роли")
    name = db.Column(db.Text, index=True, unique=True, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"
