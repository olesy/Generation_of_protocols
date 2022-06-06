from flask_principal import identity_changed, Identity, AnonymousIdentity
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import user_data_store, db, models
from app.auth import bp
from flask_security import current_user
from flask_security.utils import url_for, render_template, verify_password, flash, login_user, current_app, request, \
    get_url, logout_user, session, hash_password
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm


@bp.route("/login", methods=["GET", "POST"])
@bp.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data.replace(" ", "").lower()).first()
        if user is None or not (verify_password(form.password.data, user.password)):
            flash("Неверные данные", "danger")
        else:
            # Запомнить пользователя
            login_user(user, remember=form.remember_me.data)
            # Передаем текущего пользователя
            identity_changed.send(current_app._get_current_object(), identity = Identity(user.id))
            # запоминает страницу на которую хотели перейти пока что не авторизованы, потом когда авториз автом перейдет туда
            next_page = request.args.get("next")
            # если нет такой странице или ничего не указано
            if not next_page or url_parse(next_page).netloc != "":
                next_page = get_url("home.index")
            return redirect(next_page)
    return render_template("auth/login.html", title = "Вход", form = form)

@bp.route("/logout", methods=["GET"])
@bp.route("/logout/", methods=["GET"])
def logout():
    logout_user()
    # удаляет из сессии права пользователя (1-кому принадл права, 2-сами права)
    for key in ("identity.name", "identity.auth_type"):
        session.pop(key, None)
    # теперь права анонимного пользователя
    identity_changed.send(current_app._get_current_object(), identity = AnonymousIdentity())
    return redirect(url_for("auth.login"))

@bp.route("/registration", methods=["GET", "POST"])
@bp.route("/registration/", methods=["GET", "POST"])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        u = user_data_store.create_user(username=form.username.data,
                                        email=form.email.data,
                                        first_name=form.first_name.data,
                                        last_name=form.last_name.data,
                                        password=hash_password(form.password.data))
        db.session.add(u)
        db.session.commit()
        r = models.Role.query.get(1)
        u = models.User.query.filter(models.User.username == form.username.data).first()
        u.roles.append(r)
        db.session.add(u)
        db.session.commit()
        flash("Вы успешно зарегистрировались", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/registration.html", title = "Регистрация", form = form)