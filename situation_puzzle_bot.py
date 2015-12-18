import sys
import json
import random
import logging
import telegram
from time import sleep

try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError  # python 2


def main():
    bot = telegram.Bot('160794256:AAHJ515WhnYTwuqWKvVmcMWa3rg83DwLhKI')

    try:
        update_id = bot.getUpdates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    situation_puzzle(1, 'json_text.txt')

    while True:
        try:
            update_id = reply(bot, update_id)
        except telegram.TelegramError as e:
            if e.message in ("Bad Gateway", "Timed out"):
                sleep(1)
            elif e.message == "Unauthorized":
                update_id += 1
            else:
                raise e
        except URLError as e:
            sleep(1)


def read_data(filename):
    f = open(filename, 'r')
    return json.loads(f.read().decode('utf8'))


def situation_puzzle(new=1, filename=''):
    if (filename):
        situation_puzzle.data = read_data(filename)
        situation_puzzle.index = 0

    if (new):
        length = len(situation_puzzle.data)
        situation_puzzle.index = random.randint(0, length - 1)

    return situation_puzzle.data[situation_puzzle.index]


def reply(bot, update_id):

    for update in bot.getUpdates(offset=update_id, timeout=10):
        chat_id = update.message.chat_id
        update_id = update.update_id + 1
        message = update.message.text

        if message:
            text = ''
            if (message == 'next'):
                text = situation_puzzle(1).get('question')
            elif (message == 'answer'):
                text = situation_puzzle(0).get('answer')
            else:
                text = situation_puzzle(0).get('question')

            custom_keyboard = [['answer', 'next']]
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard,
                                                        resize_keyboard=True)
            bot.sendMessage(chat_id=chat_id,
                            text=text.encode('utf8'),
                            reply_markup=reply_markup)

    return update_id


if __name__ == '__main__':
    main()
