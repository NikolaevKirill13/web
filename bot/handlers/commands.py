from aiogram import types, exceptions

from dispatcher import dispatcher, bot
from handlers import keyboards, functions, voice


@dispatcher.message_handler(commands=["start"], commands_prefix="/")
async def start_command(message: types.Message):
    if message.chat.type !="private":
        return await message.reply(text="Бот начал работу", parse_mode="HTML")
    await message.bot.send_message(
        chat_id=message.chat.id, text=f"{message.from_user.username}, здрасте=) Для просмотра доступных команд введите /help",
        parse_mode="HTML")


@dispatcher.message_handler(commands=["help"], commands_prefix="/")
async def help_private_command(message: types.Message):
    if message.chat.type !="private":
        return await message.reply(
            text="Давайте не будем засорять общий чат.\n Обратитесь с этой командой ко мне в личные сообщения",
            parse_mode="HTML")
    await message.bot.send_message(chat_id=message.chat.id,
    text="Доступные команды: \n в личном чате - \n /faq\n в общем чате -\n /mute\n /unmute", parse_mode="HTML")


#Проверить работоспособность
"""
@dispatcher.message_handler(commands=["role"], commands_prefix="/")
async def role_command(message: types.Message):
    if message.chat.type == "private":
        return
    try:
        args = message.get_args()
        if args == 'clear':
            await message.bot.promote_chat_member(chat_id=message.chat.id, user_id=message.from_user.id, can_pin_messages = False)
            mes = await message.reply("Успешно, роль снята!")
        elif len(args) <= 16 and args != 'clear':
            await message.bot.promote_chat_member(chat_id=message.chat.id, user_id=message.from_user.id,
            can_pin_messages=True)
            await message.bot.set_chat_administrator_custom_title(chat_id=message.chat.id,
            user_id=message.from_user.id,
            custom_title = args)
            mes = await message.reply("Успешно!\nРоль появится в течение минуты.")
        elif len(args) > 16:
            await message.reply("Не могу поставить роль. Роль должна быть длинной 16 символов и менее.")
    except exceptions.CantRestrictChatOwner:
        message.reply("Ты здесь главный, тебе роль поставить не могу")


#Проверить работоспособность
@dispatcher.message_handler(commands=["pet"], commands_prefix="/")
async def pet_command(message: types.Message):
    if message.chat.type == "private" or message.reply_to_message is None:
        return 
    await message.reply_to_message.reply(f"Пользователь {message.from_user.first_name} поблагодарил пользователя {message.reply_to_message.from_user.first_name}")
    functions.send_pet(message.reply_to_message.from_user.id)
"""

@dispatcher.message_handler(commands=["mute"], commands_prefix="/")
async def mute_handler(message: types.Message):
    if message.chat.type != "supergroup" and message.chat.type != "group":
        return
    else:
        if message.reply_to_message is not None:
            user = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
            if user.status == "creator" or user.status == "administrator":
                await message.reply(text="Этот пользователь создатель группы или администратор, я не могу его замутить!!!")
            else:
                await message.reply_to_message.reply(text=f"Выдать мут пользователю id: {message.reply_to_message.from_user.id}?", reply_markup=keyboards.mute_keyboard())
        else:
            await message.reply("Нужен реплай на сообщение!")


@dispatcher.message_handler(commands=["unmute"], commands_prefix="/")
async def unmute_handler(message: types.Message):
    if message.reply_to_message is not None:
        user = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if user.status == "administrator" or user.status == "creator":
            await message.bot.restrict_chat_member(
                chat_id = message.chat.id, user_id=message.reply_to_message.from_user.id, 
                permissions=types.ChatPermissions(can_send_messages=True, can_send_games=True,
                can_send_polls=True, can_use_inline_bots=True, can_send_media_messages=True,
                can_invite_users=True, can_add_web_page_previews=True, can_send_stickers=True,
                can_send_animations=True))
        await message.reply(f"С пользователя {message.reply_to_message.from_user.id} сняты ограничения!")    
    else:
        await message.reply("Нужен реплай на сообщение!")


@dispatcher.message_handler(commands=["faq"], commands_prefix="/")
async def faq_handler(message: types.Message):
    if message.chat.type !="private":
        return
    await message.bot.send_message(chat_id=message.chat.id, text="text", reply_markup=keyboards.faq_keyboard())


@dispatcher.message_handler(commands=["recognize"], commands_prefix="/")
async def voice_handler(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Нужен реплай на сообщение с войсом.")
    else:
        if not message.reply_to_message.voice:
            await message.reply("Нужно ответить на голосовое сообщение!")
            return
        mes = await message.reply("Начинаю распознавание...")
        text = await voice.recognize_voice(await message.reply_to_message.voice.get_file())
        await message.bot.edit_message_text(chat_id=message.chat.id, text=text,
        message_id=mes.message_id, parse_mode="HTML")


@dispatcher.message_handler(content_types=[types.ContentType.NEW_CHAT_MEMBERS])
async def new_members_handler(message: types.Message):
    new_member = message.new_chat_members[0]
    #functions.push_user(new_member)
    if new_member.mention is not None:
        text =f"Добро пожаловать, {new_member.mention}.\nЭто чат для помощи и взаимообучения в программировании!"
    else:
        text =f"Добро пожаловать, {new_member.full_name}.\nЭто чат для помощи и взаимообучения в программировании!"
    await message.reply(text=text, reply_markup=keyboards.welcome_keyboard())
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
