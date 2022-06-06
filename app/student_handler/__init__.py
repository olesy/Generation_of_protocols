from flask import Blueprint
bp = Blueprint("student_handler", __name__, url_prefix="/student-handler")
from . import routes
