from aiogram import Router, F, types


group_administration_router = Router()

BAD_WORDS = ("плохой", "осёл", "собака")


@group_administration_router.message(F.chat.type == "group")
async def check_bad_words(message: types.Message):
    for word in BAD_WORDS:
        if word in message.text.lower():
            reply = message.reply_to_message
            if reply:
                await message.bot.ban_chat_member(
                    chat_id=message.chat.id,
                    user_id=reply.from_user.id
                )
                await message.reply("Пользователь забанен")

            break
