import asyncio
import aiosqlite

#this is the function of the first query
async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

#this is the function fot the second query
async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 90") as cursor:
            return await cursor.fetchall()
#Now we can fetch them concurrently by using the asyncio.gather
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users(),
    )
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())