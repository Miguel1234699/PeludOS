from fastapi import FastAPI

from app.routers import (
    auth,
    cita,
    mascota,
    medicamento,
    pedido,
    profesional_veterinario,
    recordatorio,
    resena,
    usuario,
    vacuna,
    veterinaria,
)

app = FastAPI(
    title="PeludOS API",
    description="API para la plataforma de cuidado de mascotas",
    version="0.1.0",
)

app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(mascota.router)
app.include_router(veterinaria.router)
app.include_router(profesional_veterinario.router)
app.include_router(vacuna.router)
app.include_router(medicamento.router)
app.include_router(pedido.router)
app.include_router(recordatorio.router)
app.include_router(resena.router)
app.include_router(cita.router)


@app.get("/health", tags=["Salud"])
def health_check():
    return {"status": "ok", "app": "PeludOS API"}


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
