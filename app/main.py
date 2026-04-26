import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from app.config import get_settings
from app.routers import stages, saccos, routes, search, upload
from app.db import init_pool, close_pool

log = structlog.get_logger()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("startup", environment=settings.environment)

    await init_pool()

    yield

    await close_pool()


app = FastAPI(
    title="Matatu API",
    description="Nairobi matatu route comparison engine",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stages.router)
app.include_router(saccos.router)
app.include_router(routes.router)
app.include_router(search.router)
app.include_router(upload.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
