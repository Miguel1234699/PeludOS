from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text

from app.database import Base


class Vacuna(Base):
    __tablename__ = "vacunas"

    id_vacuna = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_mascota = Column(Integer, ForeignKey("mascotas.id_mascota"), nullable=False, index=True)

    nombre_vacuna = Column(String(100), nullable=False)
    fecha_aplicacion = Column(Date, nullable=False)
    fecha_proxima = Column(Date, nullable=True)
    lote = Column(String(50), nullable=True)
    observaciones = Column(Text, nullable=True)
    activo = Column(Boolean, nullable=False, default=True)
