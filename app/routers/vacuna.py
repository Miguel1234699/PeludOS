from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.mascota import get_mascota_by_id_and_usuario
from app.crud.vacuna import (
    create_vacuna,
    desactivar_vacuna,
    get_vacuna_by_id,
    get_vacunas,
    get_vacunas_by_mascota,
    update_vacuna,
)
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.vacuna import VacunaCreate, VacunaResponse, VacunaUpdate

router = APIRouter(prefix="/vacunas", tags=["Vacunas"])


@router.post("", response_model=VacunaResponse, status_code=status.HTTP_201_CREATED)
def crear_vacuna(
    vacuna_data: VacunaCreate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mascota = get_mascota_by_id_and_usuario(
        db,
        vacuna_data.id_mascota,
        usuario_actual.id_usuario,
    )

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada",
        )

    return create_vacuna(db, vacuna_data)


@router.get("", response_model=List[VacunaResponse])
def listar_vacunas(
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_vacunas(db)


@router.get("/mascota/{id_mascota}", response_model=List[VacunaResponse])
def listar_vacunas_por_mascota(
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

    return get_vacunas_by_mascota(db, id_mascota)


@router.get("/{id_vacuna}", response_model=VacunaResponse)
def obtener_vacuna(
    id_vacuna: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    vacuna = get_vacuna_by_id(db, id_vacuna)

    if not vacuna:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacuna no encontrada",
        )

    mascota = get_mascota_by_id_and_usuario(
        db,
        vacuna.id_mascota,
        usuario_actual.id_usuario,
    )

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacuna no encontrada",
        )

    return vacuna


@router.patch("/{id_vacuna}", response_model=VacunaResponse)
def actualizar_vacuna(
    id_vacuna: int,
    vacuna_data: VacunaUpdate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    vacuna = get_vacuna_by_id(db, id_vacuna)

    if not vacuna:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacuna no encontrada",
        )

    mascota = get_mascota_by_id_and_usuario(db, vacuna.id_mascota, usuario_actual.id_usuario)

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacuna no encontrada",
        )

    return update_vacuna(db, vacuna, vacuna_data)


@router.delete("/{id_vacuna}", response_model=VacunaResponse)
def eliminar_vacuna(
    id_vacuna: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    vacuna = get_vacuna_by_id(db, id_vacuna)

    if not vacuna:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacuna no encontrada",
        )

    mascota = get_mascota_by_id_and_usuario(db, vacuna.id_mascota, usuario_actual.id_usuario)

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacuna no encontrada",
        )

    return desactivar_vacuna(db, vacuna)
