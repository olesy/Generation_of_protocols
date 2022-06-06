from flask import Blueprint
# втроенные роуты, @app_route, с помощью него мы делим маршруты сайта на пакеты. Он позволяет организовать пакетные ф-ции с одинаковыми названиями и они будут относиться к этим пакетам
'''
url_prefix - все маршруты начинаются с префикса (он автоматически применится ко всему, что находится в пакете
Соблюдение архитектурных решений, проще писать код
'''
bp = Blueprint("auth", __name__, url_prefix="/auth")
from . import routes