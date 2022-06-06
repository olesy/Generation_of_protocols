from app.models import User


def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if not user and username.isdigit():
        user = User.query.get(int(username))
    if not user:
        user = User.query.filter(User.last_name.contains(username)).first()
    # СДЕЛАТЬ ПРОВЕРКИ НА МАЛЕНЬКИЕ БОЛЬШИЕ БУКВЫ
    return user
