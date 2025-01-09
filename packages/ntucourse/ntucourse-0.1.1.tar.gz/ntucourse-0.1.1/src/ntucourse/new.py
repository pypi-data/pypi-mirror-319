import asyncio
import string
import time
from typing import Concatenate, TypedDict, Unpack

import httpx

lock = asyncio.Semaphore(5)


async def subtask(idx: str):
    print(idx, "start")
    await asyncio.sleep(3)
    print(idx, "end")


async def task(task_id: str):
    k = 3
    async with lock:
        print(task_id, "start")
        await asyncio.gather(*[subtask(f"{task_id}-{idx}") for idx in range(k)])
        print(task_id, "end")


async def main():
    async with httpx.AsyncClient() as client:
        # await asyncio.gather(*[task(f"{i}") for i in string.ascii_letters[:m]])
        st = time.perf_counter()
        await asyncio.gather(*[client.get("https://nol.ntu.edu.tw/nol/coursesearch/print_table.php?course_id=002%2050020&class=40&dpt_code=T010&ser_no=97001&semester=113-2&lang=CH") for _ in range(100)])
        print(time.perf_counter() - st)


asyncio.run(main())
