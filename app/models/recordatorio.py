from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text

from app.database import Base


class Recordatorio(Base):
    __tablename__ = "recordatorios"

    id_recordatorio = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False, index=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"), nullable=True, index=True)

    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo = Column(String(50), nullable=True)
    fecha_recordatorio = Column(DateTime(timezone=True), nullable=False)
    completado = Column(Boolean, nullable=False, default=False)
    activo = Column(Boolean, nullable=False, default=True)
