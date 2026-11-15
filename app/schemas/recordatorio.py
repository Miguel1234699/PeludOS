from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RecordatorioCreate(BaseModel):
    id_mascota: Optional[int] = None
    titulo: str
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    fecha_recordatorio: datetime


class RecordatorioUpdate(BaseModel):
    id_mascota: Optional[int] = None
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    fecha_recordatorio: Optional[datetime] = None
    completado: Optional[bool] = None


class RecordatorioResponse(BaseModel):
    id_recordatorio: int
    id_usuario: int
    id_mascota: Optional[int] = None
    titulo: str
    descripcion: Optional[str] = None
    tipo: Optional[str] = None
    fecha_recordatorio: datetime
    completado: bool
    activo: bool

    model_config = ConfigDict(from_attributes=True)
