#!/usr/bin/env python3
'''
Bot that interact with Araasac API to retrieve resources
Developer: @trukise
Email: trukise@gmail.com
'''

import config
import logging
import urllib3

import telegram
import telegram.ext

from commands.about import about
from commands.start import start
import commands.help
import commands.pictos
import commands.translate
import commands.admin

import inline.pictoInline


ARASAAC_API_KEY = ""
TELEGRAM_API_KEY = ""

global http


def main():
    #Configure logging module
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Starting logger')

    # Get ARASAAC API KEY and TELEGRAM_API_KEY
    global ARASAAC_API_KEY
    ARASAAC_API_KEY = config.loadArasaacApiKey(".arasaacApiKey")

    global TELEGRAM_API_KEY
    TELEGRAM_API_KEY = config.loadTelegramApiKey(".telegramApiKey")

    http = config.httpPool()
    logger.info(type(http))

    # Create database (sqlite3) bot.db
    config.createBotDatabase("bot.sqlite3")

    # Creating an updater object of the Bot
    updater = telegram.ext.Updater(TELEGRAM_API_KEY)

    # Start command
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
    # Help command
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('help', commands.help.help))

    # picsColor command - Get pictograms in color that contain the word passed
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('picsColor',
                                                  commands.pictos.getPictosColor,
                                                  pass_args=True))

    # picsBW command - Get pictograms in BW that contains the word passed
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('picsBW', commands.pictos.getPictosBW,
                                                  pass_args=True))
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('picsBN', commands.pictos.getPictosBW,
                                                  pass_args=True))

    # picto command - Command that init a wizard to make a search
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('pics',
                                   commands.pictos.getPics,
                                   pass_args=True))

    updater.dispatcher.add_handler(telegram.ext.CommandHandler('translate',
                                                  commands.translate.translate,
                                                  pass_args=True))
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('traducir',
                                                  commands.translate.translate,
                                                  pass_args=True))

    # About command
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('about', about))

    # Restart commmand
    updater.dispatcher.add_handler(telegram.ext.CommandHandler('restart', commands.admin.restart))

    updater.dispatcher.add_handler(telegram.ext.InlineQueryHandler(inline.pictoInline.pictoInline))

    # CallbackQueryHandlers os /pics command 1º Choose color 2º Choose language
    # 3º search property (start with, contains, end with and exactly)
    updater.dispatcher.add_handler(telegram.ext.CallbackQueryHandler(commands.pictos.getPics_stage1_color, pattern="pics.color"))
    updater.dispatcher.add_handler(telegram.ext.CallbackQueryHandler(commands.pictos.getPics_stage2_language, pattern="pics.language"))
    updater.dispatcher.add_handler(telegram.ext.CallbackQueryHandler(commands.pictos.getPics_stage3_search, pattern="pics.search"))



    updater.dispatcher.add_handler(telegram.ext.CallbackQueryHandler(commands.translate.translate_stage1_language_callback, pattern="tr.lang"))
    updater.dispatcher.add_handler(telegram.ext.CallbackQueryHandler(commands.translate.translate_stage2_word_callback, pattern="tr.word"))

    updater.dispatcher.add_handler(telegram.ext.CallbackQueryHandler(commands.translate.agenda_callback, pattern="agenda"))


    # init Bot
    updater.start_polling()
    logger.info("Bot started")
    updater.idle()


if __name__ == "__main__":
    main()
