from flask_principal import Permission, RoleNeed
from flask_security import login_required, current_user
from flask import abort, render_template, url_for, flash
from flask_security.utils import hash_password, verify_password
from werkzeug.utils import redirect

from app import user_data_store, db
from app.models import Role, StudentData
from app.profile import bp
from app.profile.forms import SearchForm, get_obj_edit_profile_form, ResetPasswordForm, EditStudentDataForm
from app.utils import get_user_by_username



@bp.route("/<username>", methods=["GET", "POST"])
@bp.route("/<username>/", methods=["GET", "POST"])
# Может войти только авторизованный пользователь
@login_required
def user_profile(username):
    user = get_user_by_username(username)
    if not user:
        return abort(404)
    permission = Permission(RoleNeed("tutor"), RoleNeed("admin"))
    if current_user.username == user.username or permission.can():
        form = SearchForm()
        if form.validate_on_submit():
            return redirect(url_for("profile.user_profile", username = form.search.data))
        return render_template("profile/user_profile.html", user = user, title = "Профиль", form = form)
    return abort(403)


@bp.route("/edit-profile/<username>", methods=["GET", "POST"])
@bp.route("/edit-profile/<username>/", methods=["GET", "POST"])
# Может войти только авторизованный пользователь
@login_required
def edit_profile(username):
    user = get_user_by_username(username)
    if not user:
        return abort(404)
    permission = Permission(RoleNeed("tutor"), RoleNeed("admin"))
    if permission.can():
        access_roles = Role.query.all() if current_user.has_role("tutor") else current_user.roles
        form = get_obj_edit_profile_form(user, access_roles)
        if form.validate_on_submit():
            new_username = form.username.data
            user.username = new_username
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.email = form.email.data
            if Permission(RoleNeed("tutor")).can():
                unchangeable_roles = set()
            else:
                # чтобы студент не смог удалить роли пользователя
                unchangeable_roles = set(user.roles) - set(current_user.roles)
            new_roles = set()
            for i in form.roles.data:
                # Достаем роль по id
                new_roles.add(Role.query.get(i))
            # Добавляем нов роли (объединение множеств)
            # (student | tutor) admin
            user.roles = list(unchangeable_roles | new_roles)
            user_data_store.put(user)
            user_data_store.commit()
            flash("Изменения сохранены", "success")
            return redirect(url_for("profile.user_profile", username = new_username))
        form.username.data = user.username
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.email.data = user.email
        return render_template("profile/edit_profile.html", user = user, title = "Редактирование профиля", form = form)
    return abort(403)

@bp.route("/reset_password/<username>", methods=["GET", "POST"])
@bp.route("/reset_password/<username>/", methods=["GET", "POST"])
# Может войти только авторизованный пользователь
@login_required
def reset_password(username):
    user = get_user_by_username(username)
    if not user:
        return abort(404)
    permission = Permission(RoleNeed("tutor"), RoleNeed("admin"))
    if current_user == user or permission.can():
        form = ResetPasswordForm()
        if form.validate_on_submit():
            if current_user == user and not (verify_password(form.current_password.data, user.password)):
                flash("Неверный пароль", "danger")
                return redirect(url_for("profile.reset_password", username = username))
            # функция получает уникальный хэш
            user.password = hash_password(form.password.data)
            user_data_store.put(user)
            user_data_store.commit()
            flash("Новый пароль успешно установлен", "success")
            return redirect(url_for("profile.user_profile", username = user.username))
        return render_template("profile/reset_password.html", user = user, title = "Профиль", form = form)
    return abort(403)


@bp.route("/edit-student-data/<username>", methods=["GET", "POST"])
@bp.route("/edit-student-data/<username>/", methods=["GET", "POST"])
# Может войти только авторизованный пользователь
@login_required
def edit_student_data(username):
    user = get_user_by_username(username)
    if not user:
        return abort(404)
    permission = Permission(RoleNeed("tutor"), RoleNeed("admin"))
    if permission.can() or current_user == user:
        form = EditStudentDataForm()
        if form.validate_on_submit():
            sure_name = form.sure_name.data
            theme_NKR = form.theme_NKR.data
            supervisor = form.supervisor.data
            NK_pages = form.NK_pages.data
            NKR_pages = form.NKR_pages.data
            slides_pages = form.slides_pages.data
            group = form.group.data
            specialize = form.specialize.data
            type_education = form.type_education.data
            department = form.department.data
            student_data = StudentData(user_id = user.id,
                                       sure_name = sure_name,
                                       theme_NKR = theme_NKR,
                                       supervisor = supervisor,
                                       NK_pages = NK_pages,
                                       NKR_pages = NKR_pages,
                                       slides_pages = slides_pages,
                                       group = group,
                                       specialize = specialize,
                                       type_education = type_education,
                                       department = department)

            db.session.add(student_data)
            db.session.commit()

            flash("Изменения сохранены", "success")
            return redirect(url_for("profile.user_profile", username = user.username))
        if user.student_data:
            form.sure_name.data = user.student_data.sure_name
            form.theme_NKR.data = user.student_data.theme_NKR
            form.supervisor.data = user.student_data.supervisor
            form.NK_pages.data = user.student_data.NK_pages
            form.NKR_pages.data = user.student_data.NKR_pages
            form.slides_pages.data = user.student_data.slides_pages
            form.group.data = user.student_data.group
            form.specialize.data = user.student_data.specialize
            form.type_education.data = user.student_data.type_education
            form.department.data = user.student_data.department

        return render_template("profile/edit_profile.html", user = user, title = "Редактирование профиля", form = form)
    return abort(403)