from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.vacuna import Vacuna
from app.schemas.vacuna import VacunaCreate, VacunaUpdate


def get_vacunas(db: Session) -> List[Vacuna]:
    return db.query(Vacuna).filter(Vacuna.activo == True).all()


def get_vacunas_by_mascota(db: Session, id_mascota: int) -> List[Vacuna]:
    return (
        db.query(Vacuna)
        .filter(Vacuna.id_mascota == id_mascota, Vacuna.activo == True)
        .all()
    )


def get_vacuna_by_id(db: Session, id_vacuna: int) -> Optional[Vacuna]:
    return (
        db.query(Vacuna)
        .filter(Vacuna.id_vacuna == id_vacuna, Vacuna.activo == True)
        .first()
    )


def create_vacuna(db: Session, vacuna_data: VacunaCreate) -> Vacuna:
    nueva_vacuna = Vacuna(**vacuna_data.model_dump())

    db.add(nueva_vacuna)
    db.commit()
    db.refresh(nueva_vacuna)

    return nueva_vacuna


def update_vacuna(db: Session, vacuna: Vacuna, vacuna_data: VacunaUpdate) -> Vacuna:
    datos = vacuna_data.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(vacuna, campo, valor)

    db.commit()
    db.refresh(vacuna)

    return vacuna


def desactivar_vacuna(db: Session, vacuna: Vacuna) -> Vacuna:
    vacuna.activo = False

    db.commit()
    db.refresh(vacuna)

    return vacuna
