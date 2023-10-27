import os
import logging
from typing import Optional

import shutil

from aiogram.types import Document, FSInputFile
from aiogram import types, Dispatcher, F
from aiogram.filters import CommandStart

from infrastructure.application import bot
from infrastructure.files import unzip, read_save

from infrastructure.config import FILES_PATH, RESULT_FILE

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.answer("Hi! I am bot. How can I help you?")


@dp.message(F.content_type == 'document')
async def zip_handler(message: types.Message):
    document: Optional[Document] = message.document

    if document.mime_type == 'application/zip':
        # Construct the download path and
        # download the document to the specified path
        download_path: str = os.path.join(FILES_PATH, f'{document.file_id}.zip')
        os.makedirs(os.path.dirname(FILES_PATH), exist_ok=True)
        await bot.download(document, download_path)
        logging.info(f'chat_id={message.chat.id}, file={document.file_name}:Zip file was downloaded')

        # Define the unzip directory and
        # process the unzipped files
        unzip_path: str = os.path.join(FILES_PATH, document.file_id)
        try:
            await unzip(download_path, unzip_path)
            logging.info(f'chat_id={message.chat.id}, file={document.file_name}:Zip file was unzipped')

            result_file_path: str = os.path.join(unzip_path, RESULT_FILE)
            await read_save(unzip_path, result_file_path)
            logging.info(f'chat_id={message.chat.id}, dir={document.file_id}:Files was proceed')

            result: FSInputFile = FSInputFile(result_file_path)
            await message.reply_document(result)
            logging.info(f'chat_id={message.chat.id}, file={RESULT_FILE}:File was send')
        except Exception as e:
            logging.error(f'chat_id={message.chat.id}. An error occurred during file processing: {e}')
            await message.answer('Error in processing .zip, try another file')
        finally:
            try:
                # Remove the unzipped directory
                shutil.rmtree(unzip_path)
                logging.info(f'chat_id={message.chat.id}, dir={document.file_id}:Directory was deleted')
            except OSError as e:
                logging.error(f'chat_id={message.chat.id}, dir={document.file_id}:{e}')
    else:
        await message.answer('File must be .zip type')
