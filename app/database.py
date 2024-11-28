import asyncpg

class DataBasePool:
    _db_pool = None

    @classmethod
    async def setup(cls):
        cls._db_pool = await asyncpg.create_pool(
            database="orangutan_database",
            user="orangutan_admin",
            password="G@V7xh!83kR*2Jz",
            host="localhost",
            port=5432
        )

    @classmethod
    async def get_pool(cls):
        if not cls._db_pool:
            raise Exception("Database connection pool is not initialized.")
        return cls._db_pool

    @classmethod
    async def teardown(cls):
        if cls._db_pool:
            await cls._db_pool.close()
            cls._db_pool = None
