from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.resena import Resena
from app.schemas.resena import ResenaCreate, ResenaUpdate


def get_resenas(db: Session) -> List[Resena]:
    return db.query(Resena).filter(Resena.activo == True).all()


def get_resenas_by_veterinaria(db: Session, id_veterinaria: int) -> List[Resena]:
    return (
        db.query(Resena)
        .filter(
            Resena.id_veterinaria == id_veterinaria,
            Resena.activo == True,
        )
        .all()
    )


def get_resenas_by_usuario(db: Session, id_usuario: int) -> List[Resena]:
    return (
        db.query(Resena)
        .filter(
            Resena.id_usuario == id_usuario,
            Resena.activo == True,
        )
        .all()
    )


def get_resena_by_id(db: Session, id_resena: int) -> Optional[Resena]:
    return (
        db.query(Resena)
        .filter(
            Resena.id_resena == id_resena,
            Resena.activo == True,
        )
        .first()
    )


def get_resena_by_id_and_usuario(
    db: Session,
    id_resena: int,
    id_usuario: int,
) -> Optional[Resena]:
    return (
        db.query(Resena)
        .filter(
            Resena.id_resena == id_resena,
            Resena.id_usuario == id_usuario,
            Resena.activo == True,
        )
        .first()
    )


def create_resena(
    db: Session,
    resena_data: ResenaCreate,
    id_usuario: int,
) -> Resena:
    nueva_resena = Resena(
        **resena_data.model_dump(),
        id_usuario=id_usuario,
    )

    db.add(nueva_resena)
    db.commit()
    db.refresh(nueva_resena)

    return nueva_resena


def update_resena(
    db: Session,
    resena: Resena,
    resena_data: ResenaUpdate,
) -> Resena:
    datos = resena_data.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(resena, campo, valor)

    db.commit()
    db.refresh(resena)

    return resena


def desactivar_resena(db: Session, resena: Resena) -> Resena:
    resena.activo = False

    db.commit()
    db.refresh(resena)

    return resena
