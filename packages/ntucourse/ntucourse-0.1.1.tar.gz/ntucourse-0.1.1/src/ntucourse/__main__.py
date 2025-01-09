import asyncio

from loguru import logger
from pydantic import TypeAdapter
from typer import Typer

from .client import AsyncClient
from .model import Course
from .quick import QueryType

app = Typer()


@app.command()
def download_all(
    *,
    max_results: int | None = None,
    concurrency: int = 10,
    use_chinese_field_names: bool = False,
    output_file: str = "courses.json",
):
    async def main():
        async with AsyncClient() as client:
            results = client.search_quick(
                semester="113-2",
                query_page_count=150,
                type=QueryType.TITLE,
                keyword="",
                page_batch_size=1,
                include_outline=True,
                concurrency=concurrency,
                tqdm={"desc": "Downloading courses"},
            )
            results = results[:max_results] if max_results else results[:]
            with open(output_file, "wb") as f:
                result_json = TypeAdapter(list[Course]).dump_json(
                    list(await results), indent=2, by_alias=use_chinese_field_names
                )
                f.write(result_json)

    asyncio.run(main())


logger.remove()
app()
