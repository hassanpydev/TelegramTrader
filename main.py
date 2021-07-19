import requests

API = '1903460584:AAFC6O9Gk6jrVWpxC91-Z2TryOWX0L7sPr8'
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
import db

allowed_users = [669065474]


def handleBoolean(status):
    return 'Enabled' if status == 1 else 'Disabled'


StartUPKeyboard = [
    ['/start', '/View Slaves'],
    ['/Done'],
]
markup = ReplyKeyboardMarkup(StartUPKeyboard,
                             one_time_keyboard=True,
                             )


def ViewUserMasters(telegram_id):
    # TODO VIEW ALL USER MASTER KEY AND RETURN THEM IN INTERACTIVE WAY
    telegramUserID = telegram_id
    user_id = db.LoadUserIDByTelegramID(telegram_id=telegramUserID)
    if user_id:
        masters = db.LoadMasters(user_id=user_id)
        keyboard = []
        for index, master in enumerate(masters):
            keyboard.append(
                [InlineKeyboardButton(f"{master.id}", callback_data=f'viewKey-{master.id}'),
                 InlineKeyboardButton("View Slaves", callback_data=f"ViewSlaves-{master.id}"),
                 InlineKeyboardButton(f"{handleBoolean(master.is_active)}",
                                      callback_data=f'changeStatus-{master.id}-{master.is_active}'),
                 InlineKeyboardButton("Delete", callback_data=f"deletemaster-{master.id}")]
            )
        reply_markup = InlineKeyboardMarkup(keyboard)

        return reply_markup
    else:
        return InlineKeyboardButton(f"Unauthorized")


def ViewMasterSlave(update: Update, context: CallbackContext):
    # TODO VIEW ALL Slaves RELATED TO Master  AND RETURN THEM IN INTERACTIVE WAY
    pass


def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("View my masters", callback_data='ViewMasters')],
        [InlineKeyboardButton("Under process", callback_data='perm')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_reply_text = 'Chose operation'
    update.message.reply_text(f"Welcome, {update.effective_user.full_name}", reply_markup=markup)
    update.message.reply_text(message_reply_text, reply_markup=reply_markup)


def UserInputHandler(update: Update, context: CallbackContext):
    command = update.message.text
    user_id = db.LoadUserIDByTelegramID(update.effective_user.id)
    if db.IsUserAuthorized(user_id) or user_id:
        if command.startswith('/addmaster'):
            if len(command.split("-")) > 1:
                db.StoreMasterKey(api=command.split("-")[-1], owner=user_id)
                update.message.reply_text("Master key has been stored successfully")
            else:
                update.message.reply_text("Please enter valid command\n/addmaster-abc123")
        else:
            update.message.reply_text("Wrong Input")
    else:
        update.message.reply_text("UNAUTHORIZED")


def ViewAllSlaves(update: Update, context: CallbackContext):
    slaves = []
    for slave in db.LoadSlaves(1):
        slaves.append([InlineKeyboardButton(slave.id, callback_data='myinfo'),
                       InlineKeyboardButton(slave.parent, callback_data='myinfo')])
    reply_markup = InlineKeyboardMarkup(slaves)
    update.message.reply_text("Slaves", reply_markup=reply_markup)


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
    # Return all master key to user
    if update.callback_query.data == 'ViewMasters':
        update.callback_query.message.reply_text("Your Masters are:",
                                                 reply_markup=ViewUserMasters(update.effective_user.id))

    # delete master key by id
    if update.callback_query.data.startswith("deletemaster"):
        master_id = update.callback_query.data.split('-')[-1]
        db.DeleteMaster(master_id)
        update.callback_query.message.reply_text("Master deleted {}".format(master_id),
                                                 reply_markup=ViewUserMasters(update.effective_user.id))
    # print all slaves by master id
    if update.callback_query.data.startswith("ViewSlaves"):
        update.callback_query.message.reply_text(
            "Viewing Slaves that belongs to: {}".format(update.callback_query.data.split('-')[-1]))
    # disable or enable master key
    if update.callback_query.data.startswith("changeStatus"):
        print(update.callback_query.data)
        master_id = update.callback_query.data.split('-')[1]
        status = update.callback_query.data.split('-')[-1]
        if int(status) != 1:
            if db.ChangeMasterStatus(master_id, 1):
                update.callback_query.message.reply_text("Master has status been enabled".title(),
                                                         reply_markup=ViewUserMasters(update.effective_user.id))
        else:
            if db.ChangeMasterStatus(master_id, 0):
                update.callback_query.message.reply_text("Master has status been disabled".title(),
                                                         reply_markup=ViewUserMasters(update.effective_user.id))
    if update.callback_query.data.startswith('viewKey'):
        master_id = update.callback_query.data.split('-')[-1]
        api_string = db.LoadMasterKey(master_id)
        update.callback_query.message.reply_text(api_string)




updater = Updater(API, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, UserInputHandler))

updater.dispatcher.add_handler(CallbackQueryHandler(getClickButtonData))
updater.start_polling()
updater.idle()
