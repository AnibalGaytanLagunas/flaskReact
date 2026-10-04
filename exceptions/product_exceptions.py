"""Excepciones de dominio para operaciones de productos."""


class ProductError(Exception):
    """Error base del dominio de productos."""


class ProductValidationError(ProductError):
    """Los datos no cumplen las reglas del negocio."""


class ProductNotFoundError(ProductError):
    def __init__(self, product_id):
        self.product_id = product_id
        super().__init__(f"El producto con id {product_id} no existe")


class ProductCreationError(ProductError):
    def __init__(self, message="No fue posible crear el producto"):
        super().__init__(message)


class ProductUpdateError(ProductError):
    def __init__(self, message="No fue posible actualizar el producto"):
        super().__init__(message)


class ProductDeleteError(ProductError):
    def __init__(self, message="No fue posible eliminar el producto"):
        super().__init__(message)


class ProductAlreadyExistsError(ProductError):
    def __init__(self, message="El producto ya existe"):
        super().__init__(message)
