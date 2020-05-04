from vkapi import longpoll
from config import *
from sql import create_data_base
import asyncio
create_data_base()

def app():
    while True:                                                                                                    # Основной цикл
        for event in longpoll.listen():
            asyncio.run(chose_handler(event))
