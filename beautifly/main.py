# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 19:54:43 2021

@author: kolomatskiy
"""

import os
import requests
import cv2
import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import filters
from dotenv import load_dotenv

"""
Simple Bot to beautify images from user.

"""

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

IMG_PATH = ''

def process_image(IMG_PATH, filterName):
    img = cv2.imread(IMG_PATH)
    flist = {
                'GreyScale':filters.greyscale,
                'Brightness Adjustment':filters.bright,
                'Sharp Effect':filters.sharpen,
                'Sepia Filter':filters.sepia,
                'GreyScale Pencil Sketch':filters.pencil_sketch_grey,
                'Colour Pencil Sketch':filters.pencil_sketch_col,
                'HDR Effect':filters.HDR,
                'Summer Effect':filters.Summer,
                'Winter Effect':filters.Winter
        }
    output_img = flist[filterName](img)
    output_img_path = IMG_PATH.replace('.png', '_{}.png'.format(filterName))
    cv2.imwrite(output_img_path, output_img)
    return output_img_path

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update, context):
    """Send a message when the command /start is issued."""
    reply_keyboard = [[KeyboardButton('Beautifly my photo!')]]
    
    # global markup
    markup = ReplyKeyboardMarkup(reply_keyboard,
                                 resize_keyboard=True,
                                 one_time_keyboard=True)
    user = update.effective_user
    update.message.reply_text('Hey!\n\nHere you can apply some filters to your photos.\n\nProject repository: https://github.com/kolomatskiy/beautifly\n\nEnjoy! ^^', reply_markup=markup)
    
def idle(update, context):
    reply_keyboard = [[KeyboardButton('Beautifly my photo!')]]
    
    # global markup
    markup = ReplyKeyboardMarkup(reply_keyboard,
                                 resize_keyboard=True,
                                 one_time_keyboard=True)
    
    update.message.reply_text(
        'Want to try one more time?', reply_markup=markup)

def beautifly(update, context):
    update.message.reply_text('Load your photo')

    
def image_handler(update, context):
    userid = update.message.from_user.id
    try:
        file = update.message.photo[-1].file_id
    except IndexError:
        file = update.message.document.file_id
    obj = context.bot.get_file(file)
    file_id, image_url = obj['file_id'], obj['file_path']
    img_data = requests.get(image_url).content
    
    
    output_folder = os.path.join('temp', str(userid))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    global IMG_PATH 
    IMG_PATH = os.path.join(output_folder,'{}.png'.format(file_id))
    with open(IMG_PATH, 'wb') as file:
        file.write(img_data)
    
    reply_keyboard = [['GreyScale',
                       'Brightness Adjustment'],
                       ['Sharp Effect',
                       'Sepia Filter'],
                       ['GreyScale Pencil Sketch',
                       'Colour Pencil Sketch'],
                       ['HDR Effect',
                       'Summer Effect',
                       'Winter Effect']]
    
    # global markup
    markup = ReplyKeyboardMarkup(reply_keyboard,
                                 resize_keyboard=True,
                                 one_time_keyboard=True)
    
    update.message.reply_text(
        'Choose filter to apply', reply_markup=markup)
    

def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    global IMG_PATH
    """Echo the user message."""
    if update.message.text == 'Beautifly my photo!':
        beautifly(update, context)
    elif update.message.text == 'GreyScale':
        output_img_path = process_image(IMG_PATH, update.message.text)
        update.message.bot.send_photo(update.message.chat.id,open(output_img_path,'rb'))
        idle(update, context)
    elif update.message.text == 'Brightness Adjustment':
        output_img_path = process_image(IMG_PATH, update.message.text)
        update.message.bot.send_photo(update.message.chat.id,open(output_img_path,'rb'))
        idle(update, context)
    elif update.message.text == 'Sharp Effect':
        output_img_path = process_image(IMG_PATH, update.message.text)
        update.message.bot.send_photo(update.message.chat.id,open(output_img_path,'rb'))
        idle(update, context)
    elif update.message.text == 'Sepia Filter':
        output_img_path = process_image(IMG_PATH, update.message.text)
        update.message.bot.send_photo(update.message.chat.id,open(output_img_path,'rb'))
        idle(update, context)
    elif update.message.text == 'GreyScale Pencil Sketch':
        output_img_path = process_image(IMG_PATH, update.message.text)
        update.message.bot.send_photo(update.message.chat.id,open(output_img_path,'rb'))
        idle(update, context)
    elif update.message.text == 'Colour Pencil Sketch':
        output_img_path = process_image(IMG_PATH, update.message.text)
        update.message.bot.send_photo(update.message.chat.id,open(output_img_path,'rb'))
        idle(update, context)
    elif update.message.text == 'HDR Effect':
        output_img_path = process_image(IMG_PATH, update.message.text)
        update.message.bot.send_photo(update.message.chat.id,open(output_img_path,'rb'))
        idle(update, context)
    elif update.message.text == 'Summer Effect':
        output_img_path = process_image(IMG_PATH, update.message.text)
        update.message.bot.send_photo(update.message.chat.id,open(output_img_path,'rb'))
        idle(update, context)
    elif update.message.text == 'Winter Effect':
        output_img_path = process_image(IMG_PATH, update.message.text)
        update.message.bot.send_photo(update.message.chat.id,open(output_img_path,'rb'))
        idle(update, context)
    else:
        update.message.reply_text('Sorry, I do not understand you.')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    update.message.reply_text('Sorry, something went wrong.')
    
def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    load_dotenv()
    updater = Updater(os.environ.get('secretToken'), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
    dispatcher.add_handler(MessageHandler(Filters.document, image_handler))
    

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    
    
    # 

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
    