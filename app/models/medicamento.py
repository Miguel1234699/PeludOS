from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text

from app.database import Base


class Medicamento(Base):
    __tablename__ = "medicamentos"

    id_medicamento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"), nullable=False, index=True)

    nombre_medicamento = Column(String(100), nullable=False)
    dosis = Column(String(100), nullable=False)
    frecuencia = Column(String(100), nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=True)
    instrucciones = Column(Text, nullable=True)
    activo = Column(Boolean, nullable=False, default=True)
