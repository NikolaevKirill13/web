import re
from aiogram import types

from dispatcher import dispatcher, bot
from handlers import keyboards, functions

from time import time


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('fao_btn'))
async def callback_fao(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        fao = functions.get_faq()
        text = fao[int(code)]["description"]
    else:
        text = "Error, i dont find this article!"
    await callback_query.message.reply(text = text)


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('mute'))
async def mute_callback_button(callback_query: types.CallbackQuery):
    counter = int(callback_query.message.reply_markup.inline_keyboard[0][0].text) + 1
    if counter + 1 <= 10:
        await callback_query.message.edit_reply_markup(reply_markup=keyboards.mute_keyboard(counter))
    else:
        user_id = callback_query.message.reply_to_message["from"].id
        await callback_query.message.edit_text(text=f"Выдан мут пользователю id: {user_id}", reply_markup="")
        await bot.restrict_chat_member(chat_id=callback_query.message.chat.id, user_id=user_id, until_date=time()+600)


@dispatcher.callback_query_handler(lambda c: c.data and c.data.startswith('welcome'))
async def mute_callback_button(callback_query: types.CallbackQuery):
    if callback_query.message.reply_to_message["from"].id != callback_query.from_user.id:
        return
    await bot.restrict_chat_member(chat_id = callback_query.message.chat.id, user_id=callback_query.message.reply_to_message["from"].id, 
            permissions=types.ChatPermissions( can_send_messages = True, can_send_games = True, 
            can_send_polls = True, can_use_inline_bots = True, can_send_media_messages = True, 
            can_invite_users = True, can_add_web_page_previews = True, can_send_stickers = True, 
            can_send_animations = True))
    await callback_query.answer(text="Ты прошел проверку",show_alert=True)
    await callback_query.message.delete()


#example of poll mute
# @dispatcher.message_handler(commands=["mute"], commands_prefix="/")
# async def test(message: types.Message):
#     await message.bot.send_poll(message.chat.id, question=f"Выдать мут пользователю id: {message.reply_to_message.from_user.id}?",
#     options=["ЗА","Против"], open_period=600, reply_to_message_id=message.reply_to_message.message_id)


# @dispatcher.poll_handler()
# async def handler_poll(poll: types.Poll):
#     if poll.options[0]["voter_count"] == 10:
#         user_id = re("\d", poll.question)
    
#         # await bot.restrict_chat_member(chat_id = callback_query.message.chat.id, user_id=callback_query.message.reply_to_message["from"].id, 
#         #     permissions=types.ChatPermissions( can_send_messages = True, can_send_games = True, 
#         #     can_send_polls = True, can_use_inline_bots = True, can_send_media_messages = True, 
#         #     can_invite_users = True, can_add_web_page_previews = True, can_send_stickers = True, 
#         #     can_send_animations = True))