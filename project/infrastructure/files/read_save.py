import asyncio
import os

from aiofiles import open


async def read_first_line(file_path, lines):
    # Read only first line from file
    async with open(file_path, 'rb') as f:
        lines.append(await f.readline())


async def save(save_path, lines):
    # Write a array of lines to result file
    async with open(save_path, 'wb') as f:
        await f.writelines(lines)
        await f.flush()


async def read_save(files_path, save_path):
    lines = []
    read_tasks = []

    # Creating tasks for reading each files and saving them to result file
    for root, _, files in os.walk(files_path):
        for file in files:
            file_path = os.path.join(root, file)
            read_tasks.append(read_first_line(file_path, lines))
    await asyncio.gather(*read_tasks)

    await save(save_path, lines)
