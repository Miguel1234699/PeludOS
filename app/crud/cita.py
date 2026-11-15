from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.cita import Cita
from app.schemas.cita import CitaCreate, CitaUpdate


def get_citas_by_usuario(db: Session, id_usuario: int) -> List[Cita]:
    return (
        db.query(Cita)
        .filter(Cita.id_usuario == id_usuario, Cita.activo == True)
        .all()
    )


def get_citas_by_mascota(
    db: Session,
    id_usuario: int,
    id_mascota: int,
) -> List[Cita]:
    return (
        db.query(Cita)
        .filter(
            Cita.id_usuario == id_usuario,
            Cita.id_mascota == id_mascota,
            Cita.activo == True,
        )
        .all()
    )


def get_citas_by_veterinaria(db: Session, id_veterinaria: int) -> List[Cita]:
    return (
        db.query(Cita)
        .filter(
            Cita.id_veterinaria == id_veterinaria,
            Cita.activo == True,
        )
        .all()
    )


def get_cita_by_id_and_usuario(
    db: Session,
    id_cita: int,
    id_usuario: int,
) -> Optional[Cita]:
    return (
        db.query(Cita)
        .filter(
            Cita.id_cita == id_cita,
            Cita.id_usuario == id_usuario,
            Cita.activo == True,
        )
        .first()
    )


def create_cita(
    db: Session,
    cita_data: CitaCreate,
    id_usuario: int,
) -> Cita:
    nueva_cita = Cita(
        **cita_data.model_dump(),
        id_usuario=id_usuario,
    )

    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)

    return nueva_cita


def update_cita(
    db: Session,
    cita: Cita,
    cita_data: CitaUpdate,
) -> Cita:
    datos = cita_data.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(cita, campo, valor)

    db.commit()
    db.refresh(cita)

    return cita


def desactivar_cita(db: Session, cita: Cita) -> Cita:
    cita.activo = False

    db.commit()
    db.refresh(cita)

    return cita
