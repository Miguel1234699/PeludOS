from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.mascota import get_mascota_by_id_and_usuario
from app.crud.medicamento import (
    create_medicamento,
    desactivar_medicamento,
    get_medicamento_by_id,
    get_medicamentos,
    get_medicamentos_by_mascota,
    update_medicamento,
)
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.medicamento import (
    MedicamentoCreate,
    MedicamentoResponse,
    MedicamentoUpdate,
)

router = APIRouter(prefix="/medicamentos", tags=["Medicamentos"])


@router.post("", response_model=MedicamentoResponse, status_code=status.HTTP_201_CREATED)
def crear_medicamento(
    medicamento_data: MedicamentoCreate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mascota = get_mascota_by_id_and_usuario(
        db,
        medicamento_data.id_mascota,
        usuario_actual.id_usuario,
    )

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mascota no encontrada",
        )

    return create_medicamento(db, medicamento_data)


@router.get("", response_model=List[MedicamentoResponse])
def listar_medicamentos(
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_medicamentos(db)


@router.get("/mascota/{id_mascota}", response_model=List[MedicamentoResponse])
def listar_medicamentos_por_mascota(
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

    return get_medicamentos_by_mascota(db, id_mascota)


@router.get("/{id_medicamento}", response_model=MedicamentoResponse)
def obtener_medicamento(
    id_medicamento: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    medicamento = get_medicamento_by_id(db, id_medicamento)

    if not medicamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicamento no encontrado",
        )

    mascota = get_mascota_by_id_and_usuario(
        db,
        medicamento.id_mascota,
        usuario_actual.id_usuario,
    )

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicamento no encontrado",
        )

    return medicamento


@router.patch("/{id_medicamento}", response_model=MedicamentoResponse)
def actualizar_medicamento(
    id_medicamento: int,
    medicamento_data: MedicamentoUpdate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    medicamento = get_medicamento_by_id(db, id_medicamento)

    if not medicamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicamento no encontrado",
        )

    mascota = get_mascota_by_id_and_usuario(
        db,
        medicamento.id_mascota,
        usuario_actual.id_usuario,
    )

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicamento no encontrado",
        )

    return update_medicamento(db, medicamento, medicamento_data)


@router.delete("/{id_medicamento}", response_model=MedicamentoResponse)
def eliminar_medicamento(
    id_medicamento: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    medicamento = get_medicamento_by_id(db, id_medicamento)

    if not medicamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicamento no encontrado",
        )

    mascota = get_mascota_by_id_and_usuario(
        db,
        medicamento.id_mascota,
        usuario_actual.id_usuario,
    )

    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medicamento no encontrado",
        )

    return desactivar_medicamento(db, medicamento)
