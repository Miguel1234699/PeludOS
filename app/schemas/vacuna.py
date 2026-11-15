from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class VacunaBase(BaseModel):
    id_mascota: int
    nombre_vacuna: str
    fecha_aplicacion: date
    fecha_proxima: Optional[date] = None
    lote: Optional[str] = None
    observaciones: Optional[str] = None


class VacunaCreate(VacunaBase):
    pass


class VacunaUpdate(BaseModel):
    nombre_vacuna: Optional[str] = None
    fecha_aplicacion: Optional[date] = None
    fecha_proxima: Optional[date] = None
    lote: Optional[str] = None
    observaciones: Optional[str] = None


class VacunaResponse(VacunaBase):
    id_vacuna: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)
