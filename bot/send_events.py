import logging
from time import sleep
from aiogram import Bot, Dispatcher, executor, types
import json
import asyncio
import logging
from aiogram.utils import exceptions, executor
from KEY import API_TOKEN
import os


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
log = logging.getLogger('broadcast')
global PATH
PATH = os.path.abspath(os.curdir)

def get_events():
    with open(PATH + "\data\events.txt", 'r', encoding='utf-8') as myfile:
        events = myfile.read()
    return events


def get_chat_id():
    with open(PATH + "\data\chat-id.json") as file:
        data = json.load(file)
        return data


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    """
    Safe messages sender
    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster() -> int:
    """
    Simple broadcaster
    :return: Count of messages
    """
    count = 0
    try:
        for chat_id in get_chat_id():
            if await send_message(int(chat_id), get_events()):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        log.info(f"{count} messages successful sent.")
    return count


executor.start(dp, broadcaster())