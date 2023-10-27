import asyncio
import os

from aiofiles import open

from infrastructure.files.identify_language import identify_language


async def read_first_line(file_path: str, lines: list, languages: set):
    # Read only first line from file and define file type
    async with open(file_path, 'rb') as f:
        lines.append(await f.readline())
        await identify_language(file_path, languages)


async def save(save_path: str, lines: list):
    # Write an array of lines to result file
    async with open(save_path, 'wb') as f:
        await f.writelines(lines)
        await f.flush()


async def read_save(files_path: str, save_path: str):
    lines: list = []
    languages: set = set()
    read_tasks: list = []

    # Create tasks for reading each files
    for root, _, files in os.walk(files_path):
        for file in files:
            file_path: str = os.path.join(root, file)
            read_tasks.append(read_first_line(file_path, lines, languages))
    await asyncio.gather(*read_tasks)

    # Process a transform of languages set to list of bytes,
    # add to all first lines and
    # save it to result file
    if not languages:
        languages.add('Not defined')
    project_type: list[bytes] = [' '.join(languages).encode('utf-8') + b'\n']
    await save(save_path, project_type + lines)
