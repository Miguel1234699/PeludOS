from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.veterinaria import (
    create_veterinaria,
    desactivar_veterinaria,
    get_veterinaria_by_id,
    get_veterinarias,
    update_veterinaria,
)
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.veterinaria import (
    VeterinariaCreate,
    VeterinariaResponse,
    VeterinariaUpdate,
)

router = APIRouter(prefix="/veterinarias", tags=["Veterinarias"])


@router.post("", response_model=VeterinariaResponse, status_code=status.HTTP_201_CREATED)
def crear_veterinaria(
    veterinaria_data: VeterinariaCreate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_veterinaria(db, veterinaria_data)


@router.get("", response_model=List[VeterinariaResponse])
def listar_veterinarias(db: Session = Depends(get_db)):
    return get_veterinarias(db)


@router.get("/{id_veterinaria}", response_model=VeterinariaResponse)
def obtener_veterinaria(
    id_veterinaria: int,
    db: Session = Depends(get_db),
):
    veterinaria = get_veterinaria_by_id(db, id_veterinaria)

    if not veterinaria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinaria no encontrada",
        )

    return veterinaria


@router.patch("/{id_veterinaria}", response_model=VeterinariaResponse)
def actualizar_veterinaria(
    id_veterinaria: int,
    veterinaria_data: VeterinariaUpdate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    veterinaria = get_veterinaria_by_id(db, id_veterinaria)

    if not veterinaria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinaria no encontrada",
        )

    return update_veterinaria(db, veterinaria, veterinaria_data)


@router.delete("/{id_veterinaria}", response_model=VeterinariaResponse)
def eliminar_veterinaria(
    id_veterinaria: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    veterinaria = get_veterinaria_by_id(db, id_veterinaria)

    if not veterinaria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinaria no encontrada",
        )

    return desactivar_veterinaria(db, veterinaria)
