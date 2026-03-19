import pytest
from typing import Any, AsyncGenerator, Callable
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import NullPool
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.db.session import get_db
from app.config import get_settings

settings = get_settings()


def make_test_app() -> FastAPI:
    from app.routers import health, trips, stages, saccos, alerts, corrections, bundle, admin, auth
    from app.middleware.rate_limit import limiter

    test_app = FastAPI()
    test_app.state.limiter = limiter

    # type: ignore[assignment]
    _handler: Callable[[Request, Any], Response] = _rate_limit_exceeded_handler
    test_app.add_exception_handler(
        RateLimitExceeded, _handler)  # type: ignore[arg-type]

    test_app.add_middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )
    test_app.include_router(health.router)
    test_app.include_router(trips.router)
    test_app.include_router(stages.router)
    test_app.include_router(saccos.router)
    test_app.include_router(alerts.router)
    test_app.include_router(corrections.router)
    test_app.include_router(bundle.router)
    test_app.include_router(admin.router)
    test_app.include_router(auth.router)
    return test_app


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    engine = create_async_engine(settings.database_url, poolclass=NullPool)

    # async_sessionmaker instead of sessionmaker — correctly typed for AsyncEngine
    TestSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with TestSessionLocal() as session:
            yield session

    app = make_test_app()
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

    await engine.dispose()
