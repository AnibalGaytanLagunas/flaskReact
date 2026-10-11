from flask import Blueprint, jsonify

admin_bp = Blueprint("admin", __name__)

AUTH_UNAVAILABLE_MESSAGE = "Ruta deshabilitada hasta implementar autenticación"


@admin_bp.route("/admin")
def admin_dashboard():
    return jsonify({"error": AUTH_UNAVAILABLE_MESSAGE}), 503


@admin_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"error": AUTH_UNAVAILABLE_MESSAGE}), 503
