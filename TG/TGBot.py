from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from DB.DB import *
from TG.Keyboards import *
from config import TGCFG
from Discord.downloader import Song
from Discord.bots import bots

REG_TEXT = "Введи регистрационный код бота на сервере(узнать можно через команды $key на нужном сервере)"
bot = Bot(TGCFG().BOT_TOKEN)


class AudioSteps(StatesGroup):
    waiting_for_channel = State()


class RegSteps(StatesGroup):
    waiting_for_code = State()
    waiting_for_discord = State()


class TGBot:
    def __init__(self):
        self.server = None
        self.file_info = ""

    def register_Steps(self, dp):
        dp.register_message_handler(self.choose_channel, state=AudioSteps.waiting_for_channel)
        dp.register_message_handler(self.get_audio, content_types=['audio'], state='*')
        dp.register_message_handler(self.reg, commands=['reg', 'register', 'r'], state='*')
        dp.register_message_handler(self.register, state=RegSteps.waiting_for_code)
        dp.register_message_handler(self.ask_discord, state=RegSteps.waiting_for_discord)

    @staticmethod
    async def downloader(file_info, filename):
        await bot.download_file(file_info.file_path, filename)

    async def get_audio(self, msg: types.Message, state: FSMContext):
        servers = list(set(UserDB().get_servers(msg.from_user.id)))
        self.file_info = msg
        await state.finish()
        if not servers:
            await msg.answer("You're not registered", reply_markup=reg_kbd())
        else:
            await msg.answer("Выбери сервер, к которому ты сейчас подключен")  # reply_markup=servers_kbd(servers)
            # bot.register_next_step_handler(msg, lambda m: choose_channel(m, file_info))
            await AudioSteps.waiting_for_channel.set()

    async def choose_channel(self, msg: types.Message, state: FSMContext):
        UserServers = list(set(UserDB().get_servers(msg.from_user.id)))
        await state.update_data(channel=msg.text)
        for serv in UserServers:
            if msg.text == serv.servers:
                await self.attach_to_ds(serv.server_id, msg)
                return
        await bot.send_message(msg.from_user.id, "You're not registered on this server")

    async def attach_to_ds(self, server_id, msg):
        print(*bots)
        for i in range(len(bots)):
            print(f"{bots[i].guild_id}  {server_id}")
            if str(bots[i].guild_id) == str(server_id):
                dsbot, queue = bots[i].bot_number, bots[i].queue
                filename = f"./music/queue/{dsbot}-song{queue + 1}.mp3"
                await self.downloader(await bot.get_file(self.file_info.audio.file_id), filename)
                song = Song(queue + 1, "", self.file_info.audio.file_name, int(self.file_info.audio.duration), True,
                            "tg", None, 1)
                bots[i].queue += 1
                bots[i].songs.append(song)
                stat = await bots[i].activate_tg()
                if not stat:
                    await bot.send_message(msg.from_user.id, "Я не подключен к каналу на этом сервере, напиши $connect в дискорде")
                return
        await bot.send_message(msg.from_user.id, "Я не запущен на этом сервере, напиши любую команду в дискорде")

    @staticmethod
    async def reg(msg, state: FSMContext):
        await state.finish()
        await bot.send_message(msg.from_user.id, REG_TEXT)
        await RegSteps.waiting_for_code.set()

    async def register(self, msg, state: FSMContext):
        await state.update_data(reg_key=msg.text)
        servers = ServerDB().get_servers()
        if msg.text == "back":
            return
        for server in servers:
            try:
                print(server.reg_key)
                if int(server.reg_key) == int(msg.text):
                    self.server = server
                    await RegSteps.waiting_for_discord.set()
                    # bot.send_message(msg.from_user.id, "Возникла ошибка, попробуй заегистрироваться еще раз")
                    return
            except Exception as ex:
                print(ex)
                await bot.send_message(msg.from_user.id, "Ошибка, попробуй еще раз. Для отмены напиши back")
                await RegSteps.waiting_for_code.set()
                return
        await bot.send_message(msg.from_user.id, "Неправильный код, попробуй еще раз. Для отмены напиши back")
        await RegSteps.waiting_for_code.set()
        return

    async def ask_discord(self, msg, state: FSMContext):
        await state.update_data(ds=msg.text)
        flag = UserDB().add_registered_user(msg, self.server.name, str(self.server.server_id))
        if flag:
            await bot.send_message(msg.from_user.id,
                             f"Успешная регистрация. Теперь ты зарегестрирован на сервер {self.server.name}")
            return
        await bot.send_message(msg.from_user.id, "Ошибка!")


async def TgBotRun():
    dp = Dispatcher(bot, storage=MemoryStorage())
    TG = TGBot()
    TG.register_Steps(dp)
    await dp.start_polling()


"""@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    match call.data:
        case "register":
            bot.send_message(call.message.chat.id, REG_TEXT)
            bot.register_next_step_handler(call.message, register)
            bot.answer_callback_query(call.id, "Регистрация")"""
