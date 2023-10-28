# Getting started with Unzip Telegram Bot

## Configuration

### Before starting need to config project/.env file:
### `BOT_TOKEN` - Telegram bot token

### After that the infrastructure/config can be modified, but it's not needed
1) ### `FILES_PATH` - directory, where files will be placed
2) ### `RESULT_FILE` - result file of all processes
3) ### `UNZIP_WORKERS` - count of workers which will be used for unzipping
4) ### `LANGUAGE_EXTENSIONS` - tuple of programming languages which used for identify type of files

## Running

1) ### `docker-compose up -d --build`
2) ### `docker-compose up`

## Functionality

### Sending .zip file for getting first lines from each unzip files