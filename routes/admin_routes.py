from flask import Blueprint, abort

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
def admin_dashboard():
    abort(401)  # Retorna un error 401 Unauthorized
    # return "login"


@admin_bp.route("/login", methods=["POST"])
def login():
    print("Datos enviados correctamente")
    return "enviado"
