from config import *
from sql import create_data_base
from telegramconfig import *

async def full_app():
    create_data_base()
    app()
    app_telegram()
asyncio.run(full_app())
         
