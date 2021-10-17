from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
# TODO: Переписать клавиатуры на aiogram

async def reg_kbd():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Регистрация", callback_data="register"))
    return markup


def servers_kbd(servers):
    kbd = ReplyKeyboardMarkup()
    added = []
    for server in servers:
        if server.servers not in added:
            kbd.add(KeyboardButton(server.servers))
        added.append(server.servers)
    return kbd
