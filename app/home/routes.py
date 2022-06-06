from app.home import bp
from flask_security.utils import render_template

@bp.route("/")
def index():
    return render_template("home/index.html")