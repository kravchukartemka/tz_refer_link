from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/ref"
database = Database(DATABASE_URL)


engine = create_async_engine('postgresql+asyncpg://postgres:postgres@localhost:5432/ref', echo=True)
Base = declarative_base()
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=True)


# открытие соединения к бд
async def init_db():
    await database.connect()


# закрытие соединения к бд
async def close_db():
    await database.disconnect()
