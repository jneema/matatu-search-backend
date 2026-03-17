import structlog
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import get_settings
from app.db.redis import get_redis_client, close_redis
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.logging import LoggingMiddleware
from app.middleware.rate_limit import limiter
from app.routers import health, trips, stages, saccos, alerts, corrections, bundle, admin

log = structlog.get_logger()
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("startup", environment=settings.environment)
    await get_redis_client()
    yield
    await close_redis()
    log.info("shutdown")


app = FastAPI(
    title="Matatu API",
    description="Nairobi matatu route comparison engine",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(trips.router)
app.include_router(stages.router)
app.include_router(saccos.router)
app.include_router(alerts.router)
app.include_router(corrections.router)
app.include_router(bundle.router)
app.include_router(admin.router)