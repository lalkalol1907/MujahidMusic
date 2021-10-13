import telebot
from config import TGCFG

bot = telebot.TeleBot(TGCFG().BOT_TOKEN)

@bot.message_handler(content_types=['audio'])
def get_audio(msg):
    bot.send_message(msg.from_user.id, "yep")
    
bot.polling()