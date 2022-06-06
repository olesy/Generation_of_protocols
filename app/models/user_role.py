from app import db
#Столбец user_id будет хранить значение из таблицы users(его id))
user_roles = db.Table("user_roles", db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
                               db.Column("role_id", db.Integer, db.ForeignKey("roles.id")),
                                schema = "public")