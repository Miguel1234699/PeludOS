from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func

from app.database import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False, index=True)

    descripcion = Column(Text, nullable=False)
    total = Column(Numeric(10, 2), nullable=False, default=0)
    estado = Column(String(30), nullable=False, default="pendiente")
    direccion_entrega = Column(Text, nullable=False)
    telefono_contacto = Column(String(20), nullable=True)
    notas = Column(Text, nullable=True)
    fecha_pedido = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    activo = Column(Boolean, nullable=False, default=True)
