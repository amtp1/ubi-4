import asyncio
from os import mkdir, path
from pathlib import Path

import yaml
from loguru import logger
from databases import Database
from sqlalchemy import MetaData, create_engine
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from objects import globals

CONFIG_DIR = Path(__file__).resolve().parent.parent
DEBUG_DIR = Path(__file__).resolve().parent
DB_DIR = Path(__file__).resolve().parent.parent
DEBUG_FOLDER = r"%s/debug" % DEBUG_DIR

async def main():
    """Main function
    1| - Check and load config.
    2| - Check debug folder and connect to logger.
    3| - Connect to database.
    4| - Connect to Telegram API
    """

    # Config
    if not Path(r"%s/config.yaml" % CONFIG_DIR).parent.exists():
        logger.error("Don't exists file is 'config.yaml")
    else:
        with open(r"%s/config.yaml" % CONFIG_DIR) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            globals.config = config

    # Debug
    if not Path(DEBUG_FOLDER).exists():
        mkdir(DEBUG_FOLDER)
    logger.add(
        r"debug/debug.log", format="{time} {level} {message}",
        level="DEBUG", rotation="1 week",
        compression="zip")

    globals.db = Database(r"sqlite:///%s/web/db.sqlite3" % DB_DIR)
    globals.metadata = MetaData()

    globals.db_engine = create_engine(str(globals.db.url))
    globals.metadata.create_all(globals.db_engine)

    # Telegram API
    globals.bot = Bot(token=globals.config["bot"]["TOKEN"], parse_mode="HTML")
    globals.dp = Dispatcher(globals.bot, storage=MemoryStorage())

    bot_info: dict = await globals.bot.get_me()
    logger.info(f"Bot username: @{bot_info.username}. Bot Id: {bot_info.id}")

    import commands

    await globals.dp.start_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")