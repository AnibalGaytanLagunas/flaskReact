"""Rutas HTTP para el recurso de productos."""

from flask import Blueprint, jsonify, request

from schemas.product_schema import (
    ProductCreateSchema,
    ProductResponseSchema,
    ProductUpdateSchema,
)
from services import product_service

api_bp = Blueprint("api", __name__)


@api_bp.route("/products", methods=["POST"])
def route_create_product():
    data = ProductCreateSchema.model_validate(request.get_json())
    product = product_service.service_create_product(
        data.name, data.price, data.description
    )
    response = ProductResponseSchema.model_validate(product)
    return jsonify(response.model_dump()), 201


@api_bp.route("/products", methods=["GET"])
def route_read_all_products():
    result = product_service.service_get_all_products()
    return jsonify(result), 200


@api_bp.route("/products/<int:product_id>", methods=["PUT"])
def route_update_product(product_id):
    # PUT es una sustitución completa: los tres campos son obligatorios.
    data = ProductUpdateSchema.model_validate(request.get_json())
    result = product_service.service_update_product(
        product_id, data.name, data.price, data.description
    )
    response = ProductResponseSchema.model_validate(result)
    return jsonify(response.model_dump()), 200


@api_bp.route("/products/<int:product_id>", methods=["DELETE"])
def route_delete_product(product_id):
    product_service.service_delete_product(product_id)
    return jsonify({"message": "Producto eliminado"}), 200


@api_bp.route("/products/<int:product_id>", methods=["GET"])
def route_get_product_by_id(product_id):
    result = product_service.service_get_product(product_id)
    response = ProductResponseSchema.model_validate(result)
    return jsonify(response.model_dump()), 200
