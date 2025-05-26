from pydantic import BaseModel
from typing import List, Optional

class Producto(BaseModel):
    nombre: str
    precio: str
    imagen: str