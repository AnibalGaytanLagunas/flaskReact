from flask import Blueprint, jsonify, request
from services import product_service
from schemas.product_schema import ProductCreateSchema, ProductResponseSchema
from pydantic import ValidationError
from exceptions.product_exceptions import ProductNotFoundError

api_bp = Blueprint('api',__name__)
#Create product
@api_bp.route('/products', methods=['POST'])
def route_create_product():        
    data = ProductCreateSchema.model_validate(request.get_json())
    product = product_service.service_create_product(
            data.name,
            data.price,
            data.description )
    response = ProductResponseSchema(**product)

    return jsonify(response.model_dump()), 201
    

@api_bp.route('/products', methods=['GET'])
def route_read_all_products():
    if request.method == 'GET':        
        result = product_service.service_get_all_products()                
        return jsonify(result), 200

    
@api_bp.route('/products/<int:product_id>',methods=['PUT'])
def route_update_product(product_id):
    if request.method == 'PUT':        
        name = request.json['name']
        price = request.json['price']
        description = request.json['description']
        result = product_service.service_update_product(product_id, name, price, description)        
        return jsonify({"message": "Producto actualizado"}), 200


@api_bp.route('/products/<int:product_id>',methods=['DELETE'])
def route_delete_product(product_id):
    product_service.service_delete_product(product_id)    
    return jsonify({
        "message": "Producto eliminado"
    }), 200


@api_bp.route('/products/<int:product_id>', methods=['GET'])
def route_get_product_by_id(product_id):
    result = product_service.service_get_product(product_id)             
    return jsonify(result), 200