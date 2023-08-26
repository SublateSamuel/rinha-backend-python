from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from api.model import Pessoa

DATABASE_URL = "postgresql+asyncpg://sublate:DaorMaelon@postgres:5432/api"
engine = create_async_engine(DATABASE_URL, echo=True, future=True, pool_size=20)

@asynccontextmanager
async def get_db():
    async with engine.connect() as conn:
        async with conn.begin():
            async_session = AsyncSession(bind=conn)
            try:
                yield async_session
            except Exception as e:
                await async_session.rollback()
                raise e
            finally:
                await async_session.close()

async def create_table():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Pessoa.metadata.create_all)
    except:
        pass