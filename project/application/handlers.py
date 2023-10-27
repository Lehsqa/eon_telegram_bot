import logging
from os.path import join
from typing import Optional

from os import makedirs, path

import shutil

from aiogram.types import Document, FSInputFile
from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart

from infrastructure.application import bot
from infrastructure.files import unzip, read_save

dp = Dispatcher()
files_path = './project/files/'


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer("Hi! I am bot. How can I help you?")


@dp.message(F.content_type == 'document')
async def zip_handler(message: types.Message):
    document: Optional[Document] = message.document

    if document.mime_type == 'application/zip':
        # Construct the download path and
        # download the document to the specified path
        download_path = join(files_path, document.file_name)
        makedirs(path.dirname(files_path), exist_ok=True)
        await bot.download(document, download_path)

        # Define the unzip directory and
        # process the unzipped files
        unzip_path = join(files_path, document.file_id)
        try:
            await unzip(download_path, unzip_path)

            result_file_path = join(unzip_path, 'result.txt')
            await read_save(unzip_path, result_file_path)

            result = FSInputFile(result_file_path)
            await message.reply_document(result)
        except Exception as e:
            logging.error(f'An error occurred during file processing: {e}')
        finally:
            try:
                # Remove the unzipped directory
                shutil.rmtree(unzip_path)
            except OSError as e:
                logging.error(f'{e}')
    else:
        await message.answer('File must be .zip type')
