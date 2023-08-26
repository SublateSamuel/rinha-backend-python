import asyncio
from celery import Celery
from api.database import get_db
from api.model import Pessoa

celery = Celery("tasks", broker="amqp://guest:guest@queue:5672//")


async def insert_in_database_async(pessoa):
    async with get_db() as session:
        session.add(Pessoa(**pessoa))
        await session.commit()


@celery.task(retry_backoff=True)
def insert_in_database(pessoa):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(insert_in_database_async(pessoa))
