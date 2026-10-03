##El servicio se encarga que las operaciones tengan sentido según las reglas del negocio.
from repositories import product_repository
from exceptions.product_exceptions import *

def service_get_all_products():
    try:
        products = product_repository.get_all_products()
    except Exception as error:
        raise ProductError() from error
    return products

def service_create_product(name, price, description):
    if not description:
        raise ValueError("Seria mejor agregar una descripcion del producto")
    
    try:
        product_id = product_repository.create_product(
        name,
        price,
        description)
    except Exception as error:
        raise ProductCreationError() from error 
    return {
        "id": product_id,
        "name": name,
        "price": price,
        "description": description
    }

def service_get_product(product_id):
    product = product_repository.get_product_by_id(product_id)
    if product is None:
        raise ProductNotFoundError(product_id)
    return product

def service_update_product(product_id, name, price, description):
    if not name:
        raise ValueError("El nombre del producto es obligatorio")
    if price <= 0:
        raise ValueError("El precio debe ser mayor que cero")
    try:
        product_repository.update_product(product_id,name,price,description)        
    except Exception as error:
        raise ProductUpdateError() from error
    
    return {
        "id": product_id,
        "name": name,
        "price": price,
        "description": description
        }

def service_delete_product(product_id):
    product = product_repository.get_product_by_id(product_id)
    if product is None:
        raise ProductNotFoundError(product_id)
    try:
        product_repository.delete_product(product_id)
    except Exception as error:
        raise ProductDeleteError() from error
    return product_id