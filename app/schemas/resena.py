from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ResenaCreate(BaseModel):
    id_veterinaria: int
    calificacion: int = Field(ge=1, le=5)
    comentario: Optional[str] = None


class ResenaUpdate(BaseModel):
    calificacion: Optional[int] = Field(default=None, ge=1, le=5)
    comentario: Optional[str] = None


class ResenaResponse(BaseModel):
    id_resena: int
    id_usuario: int
    id_veterinaria: int
    calificacion: int
    comentario: Optional[str] = None
    fecha_creacion: datetime
    activo: bool

    model_config = ConfigDict(from_attributes=True)
