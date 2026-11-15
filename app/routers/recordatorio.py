from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.mascota import get_mascota_by_id_and_usuario
from app.crud.recordatorio import (
    create_recordatorio,
    desactivar_recordatorio,
    get_recordatorio_by_id_and_usuario,
    get_recordatorios_by_mascota,
    get_recordatorios_by_usuario,
    update_recordatorio,
)
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.recordatorio import (
    RecordatorioCreate,
    RecordatorioResponse,
    RecordatorioUpdate,
)

router = APIRouter(prefix="/recordatorios", tags=["Recordatorios"])


@router.post("", response_model=RecordatorioResponse, status_code=status.HTTP_201_CREATED)
def crear_recordatorio(
    recordatorio_data: RecordatorioCreate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if recordatorio_data.id_mascota:
        mascota = get_mascota_by_id_and_usuario(
            db,
            recordatorio_data.id_mascota,
            usuario_actual.id_usuario,
        )

        if not mascota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mascota no encontrada",
            )

    return create_recordatorio(db, recordatorio_data, usuario_actual.id_usuario)


@router.get("", response_model=List[RecordatorioResponse])
def listar_recordatorios(
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_recordatorios_by_usuario(db, usuario_actual.id_usuario)


@router.get("/mascota/{id_mascota}", response_model=List[RecordatorioResponse])
def listar_recordatorios_por_mascota(
    id_mascota: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mascota = get_mascota_by_id_and_usuario(db, id_mascota, usuario_actual.id_usuario)

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada",
        )

    return get_recordatorios_by_mascota(db, usuario_actual.id_usuario, id_mascota)


@router.get("/{id_recordatorio}", response_model=RecordatorioResponse)
def obtener_recordatorio(
    id_recordatorio: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recordatorio = get_recordatorio_by_id_and_usuario(
        db,
        id_recordatorio,
        usuario_actual.id_usuario,
    )

    if not recordatorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado",
        )

    return recordatorio


@router.patch("/{id_recordatorio}", response_model=RecordatorioResponse)
def actualizar_recordatorio(
    id_recordatorio: int,
    recordatorio_data: RecordatorioUpdate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recordatorio = get_recordatorio_by_id_and_usuario(
        db,
        id_recordatorio,
        usuario_actual.id_usuario,
    )

    if not recordatorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado",
        )

    if recordatorio_data.id_mascota:
        mascota = get_mascota_by_id_and_usuario(
            db,
            recordatorio_data.id_mascota,
            usuario_actual.id_usuario,
        )

        if not mascota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mascota no encontrada",
            )

    return update_recordatorio(db, recordatorio, recordatorio_data)


@router.delete("/{id_recordatorio}", response_model=RecordatorioResponse)
def eliminar_recordatorio(
    id_recordatorio: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recordatorio = get_recordatorio_by_id_and_usuario(
        db,
        id_recordatorio,
        usuario_actual.id_usuario,
    )

    if not recordatorio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado",
        )

    return desactivar_recordatorio(db, recordatorio)
