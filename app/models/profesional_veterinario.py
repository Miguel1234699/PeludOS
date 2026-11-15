from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text

from app.database import Base


class ProfesionalVeterinario(Base):
    __tablename__ = "profesionales_veterinarios"

    id_profesional = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_veterinaria = Column(Integer, ForeignKey("veterinarias.id_veterinaria"), nullable=False, index=True)

    nombre_completo = Column(String(100), nullable=False)
    numero_tarjeta_profesional = Column(String(50), unique=True, nullable=False)
    especialidad = Column(String(100), nullable=True)
    telefono = Column(String(20), nullable=True)
    correo_electronico = Column(String(100), nullable=True)
    biografia = Column(Text, nullable=True)
    activo = Column(Boolean, nullable=False, default=True)
