from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.profesional_veterinario import (
    create_profesional,
    desactivar_profesional,
    get_profesional_by_id,
    get_profesionales,
    get_profesionales_by_veterinaria,
    update_profesional,
)
from app.crud.veterinaria import get_veterinaria_by_id
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.profesional_veterinario import (
    ProfesionalVeterinarioCreate,
    ProfesionalVeterinarioResponse,
    ProfesionalVeterinarioUpdate,
)

router = APIRouter(prefix="/profesionales-veterinarios", tags=["Profesionales Veterinarios"])


@router.post("", response_model=ProfesionalVeterinarioResponse, status_code=status.HTTP_201_CREATED)
def crear_profesional(
    profesional_data: ProfesionalVeterinarioCreate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    veterinaria = get_veterinaria_by_id(db, profesional_data.id_veterinaria)

    if not veterinaria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinaria no encontrada",
        )

    return create_profesional(db, profesional_data)


@router.get("", response_model=List[ProfesionalVeterinarioResponse])
def listar_profesionales(db: Session = Depends(get_db)):
    return get_profesionales(db)


@router.get("/veterinaria/{id_veterinaria}", response_model=List[ProfesionalVeterinarioResponse])
def listar_profesionales_por_veterinaria(
    id_veterinaria: int,
    db: Session = Depends(get_db),
):
    return get_profesionales_by_veterinaria(db, id_veterinaria)


@router.get("/{id_profesional}", response_model=ProfesionalVeterinarioResponse)
def obtener_profesional(
    id_profesional: int,
    db: Session = Depends(get_db),
):
    profesional = get_profesional_by_id(db, id_profesional)

    if not profesional:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesional veterinario no encontrado",
        )

    return profesional


@router.patch("/{id_profesional}", response_model=ProfesionalVeterinarioResponse)
def actualizar_profesional(
    id_profesional: int,
    profesional_data: ProfesionalVeterinarioUpdate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profesional = get_profesional_by_id(db, id_profesional)

    if not profesional:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesional veterinario no encontrado",
        )

    return update_profesional(db, profesional, profesional_data)


@router.delete("/{id_profesional}", response_model=ProfesionalVeterinarioResponse)
def eliminar_profesional(
    id_profesional: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    profesional = get_profesional_by_id(db, id_profesional)

    if not profesional:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profesional veterinario no encontrado",
        )

    return desactivar_profesional(db, profesional)
