import logging
from aiogram import Bot, Dispatcher, executor, types
import json
import logging
from KEY import API_TOKEN
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    global PATH
    PATH = os.path.abspath(os.curdir)
    with open(PATH + '\data\chat-id.json') as file:
        data = json.load(file)
        if str(message.chat.id) not in data:
            data.setdefault(message.chat.id)
    with open(PATH+'\data\chat-id.json', 'w') as file:
        json.dump(data, file)
    await bot.send_voice(message.chat.id, types.InputFile(PATH+'/data/audio/start.ogg'))


def get_chat_id():
    with open(PATH+'\data\chat-id.json') as file:
        data = json.load(file)
        return data


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)