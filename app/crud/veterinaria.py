from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.veterinaria import Veterinaria
from app.schemas.veterinaria import VeterinariaCreate, VeterinariaUpdate


def get_veterinarias(db: Session) -> List[Veterinaria]:
    return db.query(Veterinaria).filter(Veterinaria.activo == True).all()


def get_veterinaria_by_id(db: Session, id_veterinaria: int) -> Optional[Veterinaria]:
    return (
        db.query(Veterinaria)
        .filter(
            Veterinaria.id_veterinaria == id_veterinaria,
            Veterinaria.activo == True,
        )
        .first()
    )


def create_veterinaria(
    db: Session,
    veterinaria_data: VeterinariaCreate,
) -> Veterinaria:
    nueva_veterinaria = Veterinaria(**veterinaria_data.model_dump())

    db.add(nueva_veterinaria)
    db.commit()
    db.refresh(nueva_veterinaria)

    return nueva_veterinaria


def update_veterinaria(
    db: Session,
    veterinaria: Veterinaria,
    veterinaria_data: VeterinariaUpdate,
) -> Veterinaria:
    datos = veterinaria_data.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(veterinaria, campo, valor)

    db.commit()
    db.refresh(veterinaria)

    return veterinaria


def desactivar_veterinaria(db: Session, veterinaria: Veterinaria) -> Veterinaria:
    veterinaria.activo = False

    db.commit()
    db.refresh(veterinaria)

    return veterinaria
