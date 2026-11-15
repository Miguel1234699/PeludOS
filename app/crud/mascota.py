from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.mascota import Mascota
from app.schemas.mascota import MascotaCreate, MascotaUpdate


def get_mascotas_by_usuario(db: Session, id_usuario: int) -> List[Mascota]:
    return (
        db.query(Mascota)
        .filter(Mascota.id_usuario == id_usuario, Mascota.activo == True)
        .all()
    )


def get_mascota_by_id_and_usuario(
    db: Session,
    id_mascota: int,
    id_usuario: int,
) -> Optional[Mascota]:
    return (
        db.query(Mascota)
        .filter(
            Mascota.id_mascota == id_mascota,
            Mascota.id_usuario == id_usuario,
            Mascota.activo == True,
        )
        .first()
    )


def create_mascota(
    db: Session,
    mascota_data: MascotaCreate,
    id_usuario: int,
) -> Mascota:
    nueva_mascota = Mascota(
        **mascota_data.model_dump(),
        id_usuario=id_usuario,
    )

    db.add(nueva_mascota)
    db.commit()
    db.refresh(nueva_mascota)

    return nueva_mascota


def update_mascota(
    db: Session,
    mascota: Mascota,
    mascota_data: MascotaUpdate,
) -> Mascota:
    datos = mascota_data.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(mascota, campo, valor)

    db.commit()
    db.refresh(mascota)

    return mascota


def desactivar_mascota(db: Session, mascota: Mascota) -> Mascota:
    mascota.activo = False

    db.commit()
    db.refresh(mascota)

    return mascota
