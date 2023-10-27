import magic

from infrastructure.config.config import LANGUAGE_EXTENSIONS


async def identify_language(file_path: str, languages: set):
    # Use python-magic to determine the file type and
    # add to languages set
    mime: magic.Magic = magic.Magic()
    file_type: str = mime.from_file(file_path)
    for language in LANGUAGE_EXTENSIONS:
        if language in file_type:
            languages.add(language)
