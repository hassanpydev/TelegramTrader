import requests

API = '1903460584:AAFC6O9Gk6jrVWpxC91-Z2TryOWX0L7sPr8'
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

allowed_users = [669065474]

masters = ['abcdefee', 'ecdefee', 'webcdefee']
slaves = {masters[0]: ['123', '456', '789'],
          }


def start(update: Update, context: CallbackContext):

    keyboard = [
        [InlineKeyboardButton("print my information", callback_data='myinfo')],
        [InlineKeyboardButton("Am I permitted", callback_data='perm')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_reply_text = 'Chose operation'
    update.message.reply_text(message_reply_text, reply_markup=reply_markup)


def myinfo(update: Update, context: CallbackContext) -> None:
    update.message.reply_document(document=open('main.py', 'rb'))


def Echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("خذ _!_")


def getClickButtonData(update, context):
    if update.callback_query.data == "perm":
        if int(update.effective_user.id) in allowed_users:
            update.callback_query.message.reply_text(
                f'user{update.effective_user.full_name} is allowed to access this command')
        else:

            update.callback_query.message.reply_text(
                f'user{update.effective_user.full_name} has no permissions to access this command ')

    if update.callback_query.data == "myinfo":
        update.callback_query.message.reply_text(f'Hello {update.effective_user.id}, {update.effective_user.full_name}')


def perm(update: Update, context: CallbackContext) -> None:
    print(update.effective_user.id)
    if int(update.effective_user.id) in allowed_users:
        update.message.reply_text(f'user{update.effective_user.full_name} is allowed to access this command')
    else:

        update.message.reply_text(f'user{update.effective_user.full_name} has no permissions to access this command ')


updater = Updater(API)

updater.dispatcher.add_handler(CommandHandler('hello', myinfo))
updater.dispatcher.add_handler(CommandHandler('perm', perm))
updater.dispatcher.add_handler(CommandHandler('get', Echo))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(getClickButtonData))
updater.start_polling()
updater.idle()
