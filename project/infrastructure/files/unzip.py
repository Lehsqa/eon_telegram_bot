import asyncio
import logging
import os

from zipfile import ZipFile

from aiofiles.os import remove
from aiofiles import open


async def extract_and_save(handle, file_names, path):
    for file_name in file_names:
        # Read the file from zip archive,
        # ensure the parent directories for the file exist, creating them if necessary and
        # write the extracted data
        data = handle.read(file_name)
        file_path = os.path.join(path, file_name)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            async with open(file_path, 'wb') as fd:
                await fd.write(data)
        except IsADirectoryError:
            pass


async def unzip(zip_path, unzip_path):
    try:
        os.mkdir(unzip_path)
        with ZipFile(zip_path, 'r') as handle:
            # Unzip files and creating tasks for saving them
            files = handle.namelist()
            n_workers = 10
            chunk_size = round(len(files) / n_workers)
            if chunk_size == 0:
                chunk_size = 1
            tasks = []
            for i in range(0, len(files), chunk_size):
                file_names = files[i:(i + chunk_size)]
                tasks.append(extract_and_save(handle, file_names, unzip_path))
            await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f'An error occurred during unzipping: {e}')
    finally:
        await remove(zip_path)
