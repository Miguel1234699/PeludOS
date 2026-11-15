from typing import Optional

from pydantic import BaseModel, ConfigDict


class ProfesionalVeterinarioBase(BaseModel):
    id_veterinaria: int
    nombre_completo: str
    numero_tarjeta_profesional: str
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    biografia: Optional[str] = None


class ProfesionalVeterinarioCreate(ProfesionalVeterinarioBase):
    pass


class ProfesionalVeterinarioUpdate(BaseModel):
    id_veterinaria: Optional[int] = None
    nombre_completo: Optional[str] = None
    numero_tarjeta_profesional: Optional[str] = None
    especialidad: Optional[str] = None
    telefono: Optional[str] = None
    correo_electronico: Optional[str] = None
    biografia: Optional[str] = None
    activo: Optional[bool] = None


class ProfesionalVeterinarioResponse(ProfesionalVeterinarioBase):
    id_profesional: int
    activo: bool

    model_config = ConfigDict(from_attributes=True)
