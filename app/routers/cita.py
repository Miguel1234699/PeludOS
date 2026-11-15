from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.cita import (
    create_cita,
    desactivar_cita,
    get_cita_by_id_and_usuario,
    get_citas_by_mascota,
    get_citas_by_usuario,
    get_citas_by_veterinaria,
    update_cita,
)
from app.crud.mascota import get_mascota_by_id_and_usuario
from app.crud.profesional_veterinario import get_profesional_by_id
from app.crud.veterinaria import get_veterinaria_by_id
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.cita import CitaCreate, CitaResponse, CitaUpdate

router = APIRouter(prefix="/citas", tags=["Citas"])


@router.post("", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
def crear_cita(
    cita_data: CitaCreate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mascota = get_mascota_by_id_and_usuario(
        db,
        cita_data.id_mascota,
        usuario_actual.id_usuario,
    )

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada",
        )

    veterinaria = get_veterinaria_by_id(db, cita_data.id_veterinaria)

    if not veterinaria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veterinaria no encontrada",
        )

    if cita_data.id_profesional:
        profesional = get_profesional_by_id(db, cita_data.id_profesional)

        if not profesional:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profesional veterinario no encontrado",
            )

    return create_cita(db, cita_data, usuario_actual.id_usuario)


@router.get("", response_model=List[CitaResponse])
def listar_citas(
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_citas_by_usuario(db, usuario_actual.id_usuario)


@router.get("/mascota/{id_mascota}", response_model=List[CitaResponse])
def listar_citas_por_mascota(
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

    return get_citas_by_mascota(db, usuario_actual.id_usuario, id_mascota)


@router.get("/veterinaria/{id_veterinaria}", response_model=List[CitaResponse])
def listar_citas_por_veterinaria(
    id_veterinaria: int,
    db: Session = Depends(get_db),
):
    return get_citas_by_veterinaria(db, id_veterinaria)


@router.get("/{id_cita}", response_model=CitaResponse)
def obtener_cita(
    id_cita: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cita = get_cita_by_id_and_usuario(db, id_cita, usuario_actual.id_usuario)

    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada",
        )

    return cita


@router.patch("/{id_cita}", response_model=CitaResponse)
def actualizar_cita(
    id_cita: int,
    cita_data: CitaUpdate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cita = get_cita_by_id_and_usuario(db, id_cita, usuario_actual.id_usuario)

    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada",
        )

    if cita_data.id_mascota:
        mascota = get_mascota_by_id_and_usuario(
            db,
            cita_data.id_mascota,
            usuario_actual.id_usuario,
        )

        if not mascota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mascota no encontrada",
            )

    if cita_data.id_veterinaria:
        veterinaria = get_veterinaria_by_id(db, cita_data.id_veterinaria)

        if not veterinaria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veterinaria no encontrada",
            )

    if cita_data.id_profesional:
        profesional = get_profesional_by_id(db, cita_data.id_profesional)

        if not profesional:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Profesional veterinario no encontrado",
            )

    return update_cita(db, cita, cita_data)


@router.delete("/{id_cita}", response_model=CitaResponse)
def eliminar_cita(
    id_cita: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cita = get_cita_by_id_and_usuario(db, id_cita, usuario_actual.id_usuario)

    if not cita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada",
        )

    return desactivar_cita(db, cita)
