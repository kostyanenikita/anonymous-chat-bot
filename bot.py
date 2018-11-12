#!usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import argparse
import logging.config
import telebot

from const import (
    WELCOME_MARKUP,
    AFTER_HELP_MARKUP,
    FIND_MARKUP,
    ABORT_MARKUP,
    DROP_MARKUP,
    WELCOME_MSG,
    HELP_MSG,
    ALREADY_IN_SEARCH_MSG,
    ALREADY_HAVE_COMPANION_MSG,
    SEARCH_MSG,
    NEW_COMPANION_MSG,
    ABORT_MSG,
    NOT_IN_SEARCH_MSG,
    NO_COMPANION_MSG,
    DROP_MSG,
    LOG_CONFIG,
)


telebot.logger.setLevel('DEBUG')

parser = argparse.ArgumentParser()
parser.add_argument(
    '--token',
    dest='token',
    type=str,
    required=True,
)
args = parser.parse_args()

token = args.token
bot = telebot.TeleBot(token, threaded=False)

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

seeker = None
companions = dict()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, WELCOME_MSG, reply_markup=WELCOME_MARKUP)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, HELP_MSG, reply_markup=AFTER_HELP_MARKUP)


@bot.message_handler(commands=['find'])
def find_companion(message):
    global seeker

    if seeker == message.chat.id:
        bot.send_message(message.chat.id, ALREADY_IN_SEARCH_MSG, reply_markup=ABORT_MARKUP)
        return

    companion = companions.get(message.chat.id, None)
    if companion is not None:
        bot.send_message(message.chat.id, ALREADY_HAVE_COMPANION_MSG, reply_markup=DROP_MARKUP)

    if seeker is None:
        logger.info("In search: %s" % message.chat.id)
        seeker = message.chat.id
        bot.send_message(message.chat.id, SEARCH_MSG, reply_markup=ABORT_MARKUP)
    else:
        logger.info("Connection established: (%s, %s)" % (message.chat.id, seeker))
        companions[message.chat.id] = seeker
        bot.send_message(message.chat.id, NEW_COMPANION_MSG, reply_markup=DROP_MARKUP)
        companions[seeker] = message.chat.id
        bot.send_message(seeker, NEW_COMPANION_MSG, reply_markup=DROP_MARKUP)
        seeker = None


@bot.message_handler(commands=['abort'])
def abort_searching(message):
    global seeker

    if seeker == message.chat.id:
        seeker = None
        bot.send_message(message.chat.id, ABORT_MSG, reply_markup=FIND_MARKUP)
    else:
        bot.send_message(message.chat.id, NOT_IN_SEARCH_MSG, reply_markup=FIND_MARKUP)


@bot.message_handler(commands=['drop'])
def drop_companion(message):
    companion = companions.get(message.chat.id, None)
    if companion is None:
        bot.send_message(message.chat.id, NO_COMPANION_MSG, reply_markup=FIND_MARKUP)
    else:
        logger.info("Connection dropped: (%s, %s)" % (message.chat.id, companion))
        companions.pop(message.chat.id, None)
        bot.send_message(message.chat.id, DROP_MSG, reply_markup=FIND_MARKUP)
        companions.pop(companion, None)
        bot.send_message(companion, DROP_MSG, reply_markup=FIND_MARKUP)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    companion_chat_id = companions.get(message.chat.id, None)
    if companion_chat_id is None:
        bot.send_message(message.chat.id, NO_COMPANION_MSG, reply_markup=FIND_MARKUP)
    else:
        bot.send_message(companion_chat_id, message.text, reply_markup=DROP_MARKUP)


@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    companion_chat_id = companions.get(message.chat.id, None)
    if companion_chat_id is None:
        bot.send_message(message.chat.id, NO_COMPANION_MSG, reply_markup=FIND_MARKUP)
    else:
        bot.send_sticker(companion_chat_id, message.sticker.file_id, reply_markup=DROP_MARKUP)


if __name__ == '__main__':
    bot.polling(none_stop=True)
