from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CitaCreate(BaseModel):
    id_mascota: int
    id_veterinaria: int
    id_profesional: Optional[int] = None
    fecha_hora: datetime
    motivo: str
    notas: Optional[str] = None


class CitaUpdate(BaseModel):
    id_mascota: Optional[int] = None
    id_veterinaria: Optional[int] = None
    id_profesional: Optional[int] = None
    fecha_hora: Optional[datetime] = None
    motivo: Optional[str] = None
    estado: Optional[str] = None
    notas: Optional[str] = None


class CitaResponse(BaseModel):
    id_cita: int
    id_usuario: int
    id_mascota: int
    id_veterinaria: int
    id_profesional: Optional[int] = None
    fecha_hora: datetime
    motivo: str
    estado: str
    notas: Optional[str] = None
    fecha_creacion: datetime
    activo: bool

    model_config = ConfigDict(from_attributes=True)
