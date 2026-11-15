from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.crud.pedido import (
    create_pedido,
    desactivar_pedido,
    get_pedido_by_id_and_usuario,
    get_pedidos_by_usuario,
    update_pedido,
)
from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoUpdate

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.post("", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def crear_pedido(
    pedido_data: PedidoCreate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return create_pedido(db, pedido_data, usuario_actual.id_usuario)


@router.get("", response_model=List[PedidoResponse])
def listar_pedidos(
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return get_pedidos_by_usuario(db, usuario_actual.id_usuario)


@router.get("/{id_pedido}", response_model=PedidoResponse)
def obtener_pedido(
    id_pedido: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pedido = get_pedido_by_id_and_usuario(db, id_pedido, usuario_actual.id_usuario)

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado",
        )

    return pedido


@router.patch("/{id_pedido}", response_model=PedidoResponse)
def actualizar_pedido(
    id_pedido: int,
    pedido_data: PedidoUpdate,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pedido = get_pedido_by_id_and_usuario(db, id_pedido, usuario_actual.id_usuario)

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado",
        )

    return update_pedido(db, pedido, pedido_data)


@router.delete("/{id_pedido}", response_model=PedidoResponse)
def eliminar_pedido(
    id_pedido: int,
    usuario_actual: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pedido = get_pedido_by_id_and_usuario(db, id_pedido, usuario_actual.id_usuario)

    if not pedido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado",
        )

    return desactivar_pedido(db, pedido)
