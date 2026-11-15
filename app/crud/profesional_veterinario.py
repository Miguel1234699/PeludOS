from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.profesional_veterinario import ProfesionalVeterinario
from app.schemas.profesional_veterinario import (
    ProfesionalVeterinarioCreate,
    ProfesionalVeterinarioUpdate,
)


def get_profesionales(db: Session) -> List[ProfesionalVeterinario]:
    return (
        db.query(ProfesionalVeterinario)
        .filter(ProfesionalVeterinario.activo == True)
        .all()
    )


def get_profesionales_by_veterinaria(
    db: Session,
    id_veterinaria: int,
) -> List[ProfesionalVeterinario]:
    return (
        db.query(ProfesionalVeterinario)
        .filter(
            ProfesionalVeterinario.id_veterinaria == id_veterinaria,
            ProfesionalVeterinario.activo == True,
        )
        .all()
    )


def get_profesional_by_id(
    db: Session,
    id_profesional: int,
) -> Optional[ProfesionalVeterinario]:
    return (
        db.query(ProfesionalVeterinario)
        .filter(
            ProfesionalVeterinario.id_profesional == id_profesional,
            ProfesionalVeterinario.activo == True,
        )
        .first()
    )


def create_profesional(
    db: Session,
    profesional_data: ProfesionalVeterinarioCreate,
) -> ProfesionalVeterinario:
    nuevo_profesional = ProfesionalVeterinario(**profesional_data.model_dump())

    db.add(nuevo_profesional)
    db.commit()
    db.refresh(nuevo_profesional)

    return nuevo_profesional


def update_profesional(
    db: Session,
    profesional: ProfesionalVeterinario,
    profesional_data: ProfesionalVeterinarioUpdate,
) -> ProfesionalVeterinario:
    datos = profesional_data.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(profesional, campo, valor)

    db.commit()
    db.refresh(profesional)

    return profesional


def desactivar_profesional(
    db: Session,
    profesional: ProfesionalVeterinario,
) -> ProfesionalVeterinario:
    profesional.activo = False

    db.commit()
    db.refresh(profesional)

    return profesional
