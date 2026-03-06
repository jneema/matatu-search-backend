from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.towns.router import router as towns_router
from app.roads.router import router as roads_router
from app.destinations.router import router as destinations_router
from app.routes.router import router as routes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    # # WARNING: This deletes all data in these tables
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    # await conn.run_sync(Base.metadata.create_all)

app = FastAPI(lifespan=lifespan, title="Matatu Search API",
              version="1.0.0", docs_url="/developer/docs")

app.include_router(towns_router, prefix="/api")
app.include_router(roads_router, prefix="/api")
app.include_router(destinations_router, prefix="/api")
app.include_router(routes_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
