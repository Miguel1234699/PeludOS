from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.recordatorio import Recordatorio
from app.schemas.recordatorio import RecordatorioCreate, RecordatorioUpdate


def get_recordatorios_by_usuario(db: Session, id_usuario: int) -> List[Recordatorio]:
    return (
        db.query(Recordatorio)
        .filter(
            Recordatorio.id_usuario == id_usuario,
            Recordatorio.activo == True,
        )
        .all()
    )


def get_recordatorios_by_mascota(
    db: Session,
    id_usuario: int,
    id_mascota: int,
) -> List[Recordatorio]:
    return (
        db.query(Recordatorio)
        .filter(
            Recordatorio.id_usuario == id_usuario,
            Recordatorio.id_mascota == id_mascota,
            Recordatorio.activo == True,
        )
        .all()
    )


def get_recordatorio_by_id_and_usuario(
    db: Session,
    id_recordatorio: int,
    id_usuario: int,
) -> Optional[Recordatorio]:
    return (
        db.query(Recordatorio)
        .filter(
            Recordatorio.id_recordatorio == id_recordatorio,
            Recordatorio.id_usuario == id_usuario,
            Recordatorio.activo == True,
        )
        .first()
    )


def create_recordatorio(
    db: Session,
    recordatorio_data: RecordatorioCreate,
    id_usuario: int,
) -> Recordatorio:
    nuevo_recordatorio = Recordatorio(
        **recordatorio_data.model_dump(),
        id_usuario=id_usuario,
    )

    db.add(nuevo_recordatorio)
    db.commit()
    db.refresh(nuevo_recordatorio)

    return nuevo_recordatorio


def update_recordatorio(
    db: Session,
    recordatorio: Recordatorio,
    recordatorio_data: RecordatorioUpdate,
) -> Recordatorio:
    datos = recordatorio_data.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(recordatorio, campo, valor)

    db.commit()
    db.refresh(recordatorio)

    return recordatorio


def desactivar_recordatorio(
    db: Session,
    recordatorio: Recordatorio,
) -> Recordatorio:
    recordatorio.activo = False

    db.commit()
    db.refresh(recordatorio)

    return recordatorio
