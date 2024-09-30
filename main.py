import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import logging
import asyncio
from handlers.common import router

from database.models import async_mainm


async def main():
    await async_mainm()
    load_dotenv()
    logging.info('Пользователь вошел в чат')
    bot = Bot(token=os.getenv('API_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
