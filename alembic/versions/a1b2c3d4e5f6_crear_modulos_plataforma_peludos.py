"""crear modulos plataforma peludos

Revision ID: a1b2c3d4e5f6
Revises: ef2c4fd14a4c
Create Date: 2026-09-24
"""

from typing import Sequence, Union
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "ef2c4fd14a4c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE usuarios
    ADD COLUMN IF NOT EXISTS rol VARCHAR(20) NOT NULL DEFAULT 'cliente';

    ALTER TABLE usuarios
    ADD COLUMN IF NOT EXISTS activo BOOLEAN NOT NULL DEFAULT true;

    ALTER TABLE usuarios
    ADD COLUMN IF NOT EXISTS fecha_registro TIMESTAMP NOT NULL DEFAULT now();
    """)

    op.execute("""
    CREATE TABLE IF NOT EXISTS mascotas (
        id_mascota SERIAL PRIMARY KEY,
        id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
        nombre VARCHAR(50) NOT NULL,
        especie VARCHAR(30) NOT NULL,
        raza VARCHAR(50),
        sexo VARCHAR(10),
        fecha_nacimiento DATE,
        peso_kg NUMERIC(5,2),
        color_mascota VARCHAR(30),
        numero_chip VARCHAR(50) UNIQUE,
        foto_url TEXT,
        alergias TEXT,
        condiciones_medicas TEXT,
        activo BOOLEAN NOT NULL DEFAULT true
    );

    CREATE TABLE IF NOT EXISTS veterinarias (
        id_veterinaria SERIAL PRIMARY KEY,
        nombre_comercial VARCHAR(100) NOT NULL,
        direccion TEXT NOT NULL,
        telefono VARCHAR(20) NOT NULL,
        correo_electronico VARCHAR(100),
        horario_atencion VARCHAR(100),
        latitud NUMERIC(10,8),
        longitud NUMERIC(11,8),
        calificacion_promedio NUMERIC(3,2) NOT NULL DEFAULT 0,
        activo BOOLEAN NOT NULL DEFAULT true
    );

    CREATE TABLE IF NOT EXISTS profesionales (
        id_profesional SERIAL PRIMARY KEY,
        id_veterinaria INTEGER NOT NULL REFERENCES veterinarias(id_veterinaria),
        nombre_completo VARCHAR(100) NOT NULL,
        especialidad VARCHAR(50),
        numero_registro_profesional VARCHAR(30),
        telefono VARCHAR(20),
        correo_electronico VARCHAR(100),
        activo BOOLEAN NOT NULL DEFAULT true
    );

    CREATE TABLE IF NOT EXISTS citas_veterinarias (
        id_cita SERIAL PRIMARY KEY,
        id_mascota INTEGER NOT NULL REFERENCES mascotas(id_mascota),
        id_profesional INTEGER NOT NULL REFERENCES profesionales(id_profesional),
        id_veterinaria INTEGER NOT NULL REFERENCES veterinarias(id_veterinaria),
        fecha_cita TIMESTAMP NOT NULL,
        motivo VARCHAR(200) NOT NULL,
        estado VARCHAR(20) NOT NULL DEFAULT 'programada',
        notas TEXT,
        fecha_creacion TIMESTAMP NOT NULL DEFAULT now()
    );

    CREATE TABLE IF NOT EXISTS recordatorios (
        id_recordatorio SERIAL PRIMARY KEY,
        id_mascota INTEGER NOT NULL REFERENCES mascotas(id_mascota),
        titulo VARCHAR(100) NOT NULL,
        descripcion TEXT,
        tipo VARCHAR(30) NOT NULL,
        fecha_programada TIMESTAMP NOT NULL,
        frecuencia VARCHAR(20),
        notificado BOOLEAN NOT NULL DEFAULT false,
        fecha_notificacion TIMESTAMP,
        activo BOOLEAN NOT NULL DEFAULT true,
        fecha_creacion TIMESTAMP NOT NULL DEFAULT now()
    );

    CREATE TABLE IF NOT EXISTS medicamentos (
        id_medicamento SERIAL PRIMARY KEY,
        id_mascota INTEGER NOT NULL REFERENCES mascotas(id_mascota),
        id_recordatorio INTEGER REFERENCES recordatorios(id_recordatorio),
        nombre_medicamento VARCHAR(100) NOT NULL,
        dosis VARCHAR(50),
        unidad_medida VARCHAR(20),
        frecuencia_administracion VARCHAR(50),
        fecha_inicio DATE NOT NULL,
        fecha_fin DATE,
        observaciones TEXT,
        activo BOOLEAN NOT NULL DEFAULT true
    );

    CREATE TABLE IF NOT EXISTS vacunas (
        id_vacuna SERIAL PRIMARY KEY,
        id_mascota INTEGER NOT NULL REFERENCES mascotas(id_mascota),
        id_recordatorio INTEGER REFERENCES recordatorios(id_recordatorio),
        id_profesional INTEGER REFERENCES profesionales(id_profesional),
        nombre_vacuna VARCHAR(100) NOT NULL,
        fecha_aplicacion DATE NOT NULL,
        fecha_proxima_dosis DATE,
        numero_dosis INTEGER NOT NULL DEFAULT 1,
        lote VARCHAR(50),
        veterinario_nombre VARCHAR(100),
        fecha_creacion TIMESTAMP NOT NULL DEFAULT now()
    );

    CREATE TABLE IF NOT EXISTS productos (
        id_producto SERIAL PRIMARY KEY,
        id_veterinaria INTEGER NOT NULL REFERENCES veterinarias(id_veterinaria),
        nombre_producto VARCHAR(100) NOT NULL,
        descripcion TEXT,
        categoria VARCHAR(30),
        precio_compra NUMERIC(10,2) NOT NULL,
        precio_venta NUMERIC(10,2) NOT NULL,
        stock INTEGER NOT NULL DEFAULT 0,
        unidad_medida VARCHAR(20),
        imagen_url TEXT,
        activo BOOLEAN NOT NULL DEFAULT true,
        fecha_creacion TIMESTAMP NOT NULL DEFAULT now()
    );

    CREATE TABLE IF NOT EXISTS carrito_compras (
        id_carrito SERIAL PRIMARY KEY,
        id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
        fecha_creacion TIMESTAMP NOT NULL DEFAULT now(),
        estado VARCHAR(20) NOT NULL DEFAULT 'activo'
    );

    CREATE TABLE IF NOT EXISTS detalle_carrito (
        id_detalle_carrito SERIAL PRIMARY KEY,
        id_carrito INTEGER NOT NULL REFERENCES carrito_compras(id_carrito),
        id_producto INTEGER NOT NULL REFERENCES productos(id_producto),
        cantidad INTEGER NOT NULL DEFAULT 1,
        precio_unitario NUMERIC(10,2) NOT NULL,
        subtotal NUMERIC(10,2) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS pedidos (
        id_pedido SERIAL PRIMARY KEY,
        id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
        id_veterinaria INTEGER NOT NULL REFERENCES veterinarias(id_veterinaria),
        id_carrito INTEGER NOT NULL REFERENCES carrito_compras(id_carrito),
        fecha_pedido TIMESTAMP NOT NULL DEFAULT now(),
        total NUMERIC(10,2) NOT NULL,
        estado_pedido VARCHAR(30) NOT NULL DEFAULT 'pendiente',
        metodo_pago VARCHAR(30),
        direccion_entrega TEXT NOT NULL,
        notas TEXT,
        fecha_entrega TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS resenas (
        id_resena SERIAL PRIMARY KEY,
        id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
        id_veterinaria INTEGER NOT NULL REFERENCES veterinarias(id_veterinaria),
        id_pedido INTEGER REFERENCES pedidos(id_pedido),
        calificacion INTEGER NOT NULL CHECK (calificacion >= 1 AND calificacion <= 5),
        comentario TEXT,
        fecha_creacion TIMESTAMP NOT NULL DEFAULT now(),
        activo BOOLEAN NOT NULL DEFAULT true
    );

    CREATE TABLE IF NOT EXISTS mensajes (
        id_mensaje SERIAL PRIMARY KEY,
        id_usuario_remitente INTEGER NOT NULL REFERENCES usuarios(id_usuario),
        id_usuario_destinatario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
        id_veterinaria INTEGER REFERENCES veterinarias(id_veterinaria),
        id_cita INTEGER REFERENCES citas_veterinarias(id_cita),
        contenido TEXT NOT NULL,
        leido BOOLEAN NOT NULL DEFAULT false,
        fecha_envio TIMESTAMP NOT NULL DEFAULT now()
    );
    """)

    op.execute("""
    CREATE INDEX IF NOT EXISTS ix_mascotas_id_usuario ON mascotas(id_usuario);
    CREATE INDEX IF NOT EXISTS ix_profesionales_id_veterinaria ON profesionales(id_veterinaria);
    CREATE INDEX IF NOT EXISTS ix_citas_id_mascota ON citas_veterinarias(id_mascota);
    CREATE INDEX IF NOT EXISTS ix_recordatorios_id_mascota ON recordatorios(id_mascota);
    CREATE INDEX IF NOT EXISTS ix_medicamentos_id_mascota ON medicamentos(id_mascota);
    CREATE INDEX IF NOT EXISTS ix_vacunas_id_mascota ON vacunas(id_mascota);
    CREATE INDEX IF NOT EXISTS ix_productos_id_veterinaria ON productos(id_veterinaria);
    CREATE INDEX IF NOT EXISTS ix_carrito_id_usuario ON carrito_compras(id_usuario);
    CREATE INDEX IF NOT EXISTS ix_pedidos_id_usuario ON pedidos(id_usuario);
    CREATE INDEX IF NOT EXISTS ix_resenas_id_veterinaria ON resenas(id_veterinaria);
    CREATE INDEX IF NOT EXISTS ix_mensajes_destinatario ON mensajes(id_usuario_destinatario);
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS mensajes CASCADE;
    DROP TABLE IF EXISTS resenas CASCADE;
    DROP TABLE IF EXISTS pedidos CASCADE;
    DROP TABLE IF EXISTS detalle_carrito CASCADE;
    DROP TABLE IF EXISTS carrito_compras CASCADE;
    DROP TABLE IF EXISTS productos CASCADE;
    DROP TABLE IF EXISTS vacunas CASCADE;
    DROP TABLE IF EXISTS medicamentos CASCADE;
    DROP TABLE IF EXISTS recordatorios CASCADE;
    DROP TABLE IF EXISTS citas_veterinarias CASCADE;
    DROP TABLE IF EXISTS profesionales CASCADE;
    DROP TABLE IF EXISTS veterinarias CASCADE;
    DROP TABLE IF EXISTS mascotas CASCADE;
    """)
