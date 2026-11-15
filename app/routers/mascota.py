from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.mascota import (
    create_mascota,
    desactivar_mascota,
    get_mascota_by_id_and_usuario,
    get_mascotas_by_usuario,
    update_mascota,
)
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.mascota import MascotaCreate, MascotaResponse, MascotaUpdate

router = APIRouter(prefix="/mascotas", tags=["Mascotas"])


@router.post("", response_model=MascotaResponse, status_code=status.HTTP_201_CREATED)
def crear_mascota(
    mascota_data: MascotaCreate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_mascota(db, mascota_data, usuario_actual.id_usuario)


@router.get("", response_model=List[MascotaResponse])
def listar_mascotas(
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_mascotas_by_usuario(db, usuario_actual.id_usuario)


@router.get("/{id_mascota}", response_model=MascotaResponse)
def obtener_mascota(
    id_mascota: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mascota = get_mascota_by_id_and_usuario(
        db,
        id_mascota,
        usuario_actual.id_usuario,
    )

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada",
        )

    return mascota


@router.patch("/{id_mascota}", response_model=MascotaResponse)
def actualizar_mascota(
    id_mascota: int,
    mascota_data: MascotaUpdate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mascota = get_mascota_by_id_and_usuario(
        db,
        id_mascota,
        usuario_actual.id_usuario,
    )

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada",
        )

    return update_mascota(db, mascota, mascota_data)


@router.delete("/{id_mascota}", response_model=MascotaResponse)
def eliminar_mascota(
    id_mascota: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mascota = get_mascota_by_id_and_usuario(
        db,
        id_mascota,
        usuario_actual.id_usuario,
    )

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada",
        )

    return desactivar_mascota(db, mascota)
