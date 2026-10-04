"""Esquemas de validación y respuesta para productos."""

from pydantic import BaseModel, ConfigDict, Field


class ProductInputSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(min_length=1)
    price: float = Field(gt=0, allow_inf_nan=False)
    description: str = Field(min_length=1)


class ProductCreateSchema(ProductInputSchema):
    """Datos requeridos para crear un producto."""


class ProductUpdateSchema(ProductInputSchema):
    """PUT reemplaza el recurso completo: requiere todos los campos."""


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    price: float
    description: str
