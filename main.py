from fastapi import  FastAPI
from contextlib import asynccontextmanager
from database import  engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routers import route_router

# Create tables on startup (In production, use Alembic)
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    # # WARNING: This deletes all data in these tables
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    # await conn.run_sync(Base.metadata.create_all)

app = FastAPI(lifespan=lifespan, title="Matatu Search API", version="1.0.0", docs_url="/docs")
app.include_router(route_router.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)