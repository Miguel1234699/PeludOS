from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MedicamentoBase(BaseModel):
    id_mascota: int
    nombre_medicamento: str
    dosis: str
    frecuencia: Optional[str] = None
    fecha_inicio: date
    fecha_fin: Optional[date] = None
    instrucciones: Optional[str] = None


class MedicamentoCreate(MedicamentoBase):
    pass


class MedicamentoUpdate(BaseModel):
    nombre_medicamento: Optional[str] = None
    dosis: Optional[str] = None
    frecuencia: Optional[str] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    instrucciones: Optional[str] = None


class MedicamentoResponse(MedicamentoBase):
    id_medicamento: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)
