import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import engine, Base, get_db
from app.services.seed_service import SeedService
from app.api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas en SQLite
    Base.metadata.create_all(bind=engine)
    # Poblar base de datos con contenido oficial si está vacía
    db = next(get_db())
    try:
        SeedService.seed_database(db)
    finally:
        db.close()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# Rutas de frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend", "templates")

# Montar archivos estáticos
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Incluir API routers
app.include_router(api_router, prefix="/api", tags=["API"])

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "project_name": settings.PROJECT_NAME,
            "cargo": settings.CARGO,
            "opec": settings.OPEC,
            "ficha": settings.MANUAL_FUNCIONES_FICHA,
            "vacantes": settings.VACANTES,
            "ciudades": ", ".join(settings.CIUDADES_VACANTES)
        }
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
