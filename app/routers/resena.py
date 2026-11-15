from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.resena import (
    create_resena,
    desactivar_resena,
    get_resena_by_id,
    get_resena_by_id_and_usuario,
    get_resenas,
    get_resenas_by_usuario,
    get_resenas_by_veterinaria,
    update_resena,
)
from app.crud.veterinaria import get_veterinaria_by_id
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.resena import ResenaCreate, ResenaResponse, ResenaUpdate

router = APIRouter(prefix="/resenas", tags=["Reseñas"])


@router.post("", response_model=ResenaResponse, status_code=status.HTTP_201_CREATED)
def crear_resena(
    resena_data: ResenaCreate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    veterinaria = get_veterinaria_by_id(db, resena_data.id_veterinaria)

    if not veterinaria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinaria no encontrada",
        )

    return create_resena(db, resena_data, usuario_actual.id_usuario)


@router.get("", response_model=List[ResenaResponse])
def listar_resenas(db: Session = Depends(get_db)):
    return get_resenas(db)


@router.get("/me", response_model=List[ResenaResponse])
def listar_mis_resenas(
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_resenas_by_usuario(db, usuario_actual.id_usuario)


@router.get("/veterinaria/{id_veterinaria}", response_model=List[ResenaResponse])
def listar_resenas_por_veterinaria(
    id_veterinaria: int,
    db: Session = Depends(get_db),
):
    return get_resenas_by_veterinaria(db, id_veterinaria)


@router.get("/{id_resena}", response_model=ResenaResponse)
def obtener_resena(
    id_resena: int,
    db: Session = Depends(get_db),
):
    resena = get_resena_by_id(db, id_resena)

    if not resena:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reseña no encontrada",
        )

    return resena


@router.patch("/{id_resena}", response_model=ResenaResponse)
def actualizar_resena(
    id_resena: int,
    resena_data: ResenaUpdate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resena = get_resena_by_id_and_usuario(db, id_resena, usuario_actual.id_usuario)

    if not resena:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reseña no encontrada",
        )

    return update_resena(db, resena, resena_data)


@router.delete("/{id_resena}", response_model=ResenaResponse)
def eliminar_resena(
    id_resena: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resena = get_resena_by_id_and_usuario(db, id_resena, usuario_actual.id_usuario)

    if not resena:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reseña no encontrada",
        )

    return desactivar_resena(db, resena)
