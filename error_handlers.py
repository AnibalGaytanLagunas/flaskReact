from flask import jsonify
from pydantic import ValidationError

from exceptions.product_exceptions import (
    ProductNotFoundError,
    ProductCreationError,
    ProductUpdateError,
    ProductDeleteError,
    ProductAlreadyExistsError,
    ProductError
)


def register_error_handlers(app):



    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            "error": "Datos inválidos",
            "details": error.errors()
        }), 400


    @app.errorhandler(ProductError)
    def handle_product_error(error):
        return jsonify({
            "error": str(error)
        }), 500

    @app.errorhandler(ProductNotFoundError)
    def handle_product_not_found(error):

        return jsonify({
            "error": str(error)
        }), 404


    @app.errorhandler(ProductAlreadyExistsError)
    def handle_product_already_exists(error):

        return jsonify({
            "error": str(error)
        }), 409


    @app.errorhandler(ProductCreationError)
    def handle_product_creation_error(error):

        return jsonify({
            "error": str(error)
        }), 500


    @app.errorhandler(ProductUpdateError)
    def handle_product_update_error(error):

        return jsonify({
            "error": str(error)
        }), 500


    @app.errorhandler(ProductDeleteError)
    def handle_product_delete_error(error):

        return jsonify({
            "error": str(error)
        }), 500


    @app.errorhandler(404)
    def handle_http_not_found(error):

        return jsonify({
            "error": "Endpoint no encontrado"
        }), 404


    @app.errorhandler(500)
    def handle_internal_server_error(error):

        app.logger.exception(error)

        return jsonify({
            "error": "Error interno del servidor"
        }), 500