# -*- coding: utf-8 -*-
from __future__ import absolute_import

import telebot


def generate_markup(*replies):
    markup = telebot.types.ReplyKeyboardMarkup()
    for reply in replies:
        button = telebot.types.KeyboardButton('/' + reply)
        markup.add(button)
    return markup


WELCOME_MARKUP = generate_markup('find', 'help')
AFTER_HELP_MARKUP = generate_markup('find', 'drop')
FIND_MARKUP = generate_markup('find')
ABORT_MARKUP = generate_markup('abort')
DROP_MARKUP = generate_markup('drop')

WELCOME_MSG = 'Hello! If you want to find an anonymous companion, please use the \"/find\" command.'
HELP_MSG = 'Use \"/find\" to find a new companion, \"/drop\" to drop an existing one, \"/abort\" to abort search.'
ALREADY_IN_SEARCH_MSG = 'You are already in search.'
ALREADY_HAVE_COMPANION_MSG = 'You already have a companion'
SEARCH_MSG = 'Searching for a companion.'
NEW_COMPANION_MSG = 'Companion was found.'
ABORT_MSG = 'Search was aborted.'
NOT_IN_SEARCH_MSG = 'You are not in search.'
NO_COMPANION_MSG = 'Sorry, but you don\'t have any companion.'
DROP_MSG = 'Companion was dropped.'

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'default': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 5,
            'filename': 'default.log',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': {
                'default',
            },
        },
    },
}
