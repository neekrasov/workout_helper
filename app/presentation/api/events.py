from blacksheep import Application
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine


async def on_shutdown(app: Application):
    engine: AsyncEngine = app.services.build_provider().get(AsyncEngine)
    redis: Redis = app.services.build_provider().get(Redis)

    if engine:
        await engine.dispose()
    if redis:
        await redis.close()
