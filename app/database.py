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
            port=5432,
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


async def execute_db_query(query, *args):

    pool = await DataBasePool.get_pool()
    async with pool.acquire() as connection:
        try:
            result = await connection.fetch(query, *args)
            return result
        except Exception as e:
            print(f"Database query failed: {e}")
            raise e


# Maybe will be useful in the future
# async def execute_db_transaction(queries_with_params):
#     pool = await DataBasePool.get_pool()
#     async with pool.acquire() as connection:
#         async with connection.transaction():
#             try:
#                 results = []
#                 for query, params in queries_with_params:
#                     result = await connection.fetch(query, *params)
#                     results.append(result)
#                 return results
#             except Exception as e:
#                 print(f"Database transaction query failed: {e}")
#                 raise e
