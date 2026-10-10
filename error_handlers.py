"""Manejadores centralizados de errores HTTP y del dominio."""

from flask import jsonify
from pydantic import ValidationError
from werkzeug.exceptions import BadRequest, HTTPException, UnsupportedMediaType

from exceptions.product_exceptions import (
    ProductAlreadyExistsError,
    ProductCreationError,
    ProductDeleteError,
    ProductError,
    ProductNotFoundError,
    ProductUpdateError,
    ProductValidationError,
)


def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        details = [
            {
                "field": ".".join(str(part) for part in item.get("loc", ())),
                "message": item.get("msg", "Dato inválido"),
                "type": item.get("type", "value_error"),
            }
            for item in error.errors()
        ]
        return jsonify({"error": "Datos inválidos", "details": details}), 400

    @app.errorhandler(ProductValidationError)
    def handle_product_validation_error(error):
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(ProductNotFoundError)
    def handle_product_not_found(error):
        return jsonify({"error": str(error)}), 404

    @app.errorhandler(ProductAlreadyExistsError)
    def handle_product_already_exists(error):
        return jsonify({"error": str(error)}), 409

    @app.errorhandler(ProductCreationError)
    def handle_product_creation_error(error):
        app.logger.error("No se pudo crear el producto: %s", error)
        return jsonify({"error": "No fue posible crear el producto"}), 500

    @app.errorhandler(ProductUpdateError)
    def handle_product_update_error(error):
        app.logger.error("No se pudo actualizar el producto: %s", error)
        return jsonify({"error": "No fue posible actualizar el producto"}), 500

    @app.errorhandler(ProductDeleteError)
    def handle_product_delete_error(error):
        app.logger.error("No se pudo eliminar el producto: %s", error)
        return jsonify({"error": "No fue posible eliminar el producto"}), 500

    @app.errorhandler(ProductError)
    def handle_product_error(error):
        app.logger.error("Error de servicio de productos: %s", error)
        return jsonify({"error": "Error al procesar la operación de productos"}), 500

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        return jsonify({"error": "Solicitud incorrecta o JSON inválido"}), 400

    @app.errorhandler(UnsupportedMediaType)
    def handle_unsupported_media_type(error):
        return jsonify({"error": "El contenido debe enviarse como application/json"}), 415

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        if error.code == 404:
            message = "Endpoint no encontrado"
        else:
            message = error.name

        return jsonify({"error": message}), error.code

    @app.errorhandler(500)
    def handle_internal_server_error(error):
        app.logger.error("Error interno del servidor: %s", error)
        return jsonify({"error": "Error interno del servidor"}), 500
