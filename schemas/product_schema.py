##el esquema se encarga que los datos tengan la estructura y tipos correctos

from pydantic import BaseModel, Field

class ProductCreateSchema(BaseModel):
  name: str = Field(min_length=1)
  price: float = Field(gt=0)
  description: str

class ProductResponseSchema(BaseModel):
  id: int
  name: str
  price: float
  description: str