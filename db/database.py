from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLite Database
DATABASE_URL = "sqlite+aiosqlite:///./wallet.db"

# Create Async Engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create Async Session
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# Base Model
Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
