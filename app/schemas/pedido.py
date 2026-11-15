from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PedidoCreate(BaseModel):
    descripcion: str
    total: Decimal
    direccion_entrega: str
    telefono_contacto: Optional[str] = None
    notas: Optional[str] = None


class PedidoUpdate(BaseModel):
    descripcion: Optional[str] = None
    total: Optional[Decimal] = None
    estado: Optional[str] = None
    direccion_entrega: Optional[str] = None
    telefono_contacto: Optional[str] = None
    notas: Optional[str] = None


class PedidoResponse(BaseModel):
    id_pedido: int
    id_usuario: int
    descripcion: str
    total: Decimal
    estado: str
    direccion_entrega: str
    telefono_contacto: Optional[str] = None
    notas: Optional[str] = None
    fecha_pedido: datetime
    activo: bool

    model_config = ConfigDict(from_attributes=True)
