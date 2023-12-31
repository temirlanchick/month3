import asyncio
from aiogram.types import BotCommand
from logging import basicConfig


from HW1 import dp, bot
from handlers import (
    start_router,
    shop_router,
    echo_router,
    pic_router,
    questions_router,
    scheduler_router,
    group_administration_router
)


async def main(on_startup=None):
    await bot.set_my_commands(
        [
            BotCommand(command='start', description='Главная'),
            BotCommand(command='picture', description='Картинка'),
            BotCommand(command='ask', description='Диалог'),
            BotCommand(command='shop', description='Магазин')
        ]
    )

    # роутеры

    dp.include_router(start_router)
    dp.include_router(shop_router)
    dp.include_router(pic_router)
    dp.include_router(questions_router)
    dp.include_router(scheduler_router)
    dp.include_router(group_administration_router)
    # в самом конце
    dp.include_router(echo_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    basicConfig(level='INFO')
    asyncio.run(main())
