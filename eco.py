import aiohttp
import asyncio

from loguru import logger


async def subscribe_on_eco(worker: str, queue: asyncio.Queue) -> None:
    while not queue.empty():
        email = await queue.get()

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://836gwkd0c3.execute-api.us-west-1.amazonaws.com/production/waitlist",
                json={"email": email}
            ) as resp:
                if resp.status == 200:
                    logger.success(
                        f"{worker} - {email} successfully registered")
                else:
                    logger.error(f"{worker} - {email} - error!")


async def main(emails):
    queue = asyncio.Queue()

    for email in emails:
        queue.put_nowait(email)

    tasks = [asyncio.create_task(subscribe_on_eco(
             f"Worker {i}", queue)) for i in range(5)]

    await asyncio.gather(*tasks)
