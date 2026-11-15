from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, PedidoUpdate


def get_pedidos_by_usuario(db: Session, id_usuario: int) -> List[Pedido]:
    return (
        db.query(Pedido)
        .filter(Pedido.id_usuario == id_usuario, Pedido.activo == True)
        .all()
    )


def get_pedido_by_id_and_usuario(
    db: Session,
    id_pedido: int,
    id_usuario: int,
) -> Optional[Pedido]:
    return (
        db.query(Pedido)
        .filter(
            Pedido.id_pedido == id_pedido,
            Pedido.id_usuario == id_usuario,
            Pedido.activo == True,
        )
        .first()
    )


def create_pedido(
    db: Session,
    pedido_data: PedidoCreate,
    id_usuario: int,
) -> Pedido:
    nuevo_pedido = Pedido(
        **pedido_data.model_dump(),
        id_usuario=id_usuario,
    )

    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)

    return nuevo_pedido


def update_pedido(
    db: Session,
    pedido: Pedido,
    pedido_data: PedidoUpdate,
) -> Pedido:
    datos = pedido_data.model_dump(exclude_unset=True)

    for campo, valor in datos.items():
        setattr(pedido, campo, valor)

    db.commit()
    db.refresh(pedido)

    return pedido


def desactivar_pedido(db: Session, pedido: Pedido) -> Pedido:
    pedido.activo = False

    db.commit()
    db.refresh(pedido)

    return pedido
