from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext


# /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я бот для отправки напоминаний.')
    update.message.reply_text('Используй команду /reminder, чтобы установить напоминание.')


# /reminder
def set_reminder(update: Update, context: CallbackContext):
    user = update.message.from_user
    chat_id = update.message.chat_id
    tel_id = user.id
    test = context.args[0]
    date = context.args[1]
    time = context.args[2]
    answer_time = int(context.args[3])

    keyboard = [
        [InlineKeyboardButton("Выполнено", callback_data='done')],
        [InlineKeyboardButton("Не сделано", callback_data='not_done')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = f"Напоминание для тебя:nn{test}nДата: {date}nВремя: {time}"
    update.message.reply_text(message, reply_markup=reply_markup)

    context.job_queue.run_once(notify_manager, answer_time, context=(chat_id, tel_id))


def notify_manager(context: CallbackContext):
    chat_id, tel_id = context.job.context
    message = f"Сотрудник с telegram id {tel_id} ответил на напоминание."
    context.bot.send_message(chat_id=chat_id, text=message)


def button_click(update: Update, context: CallbackContext):
    query = update.callback_query
    answer = query.data
    tel_id = query.from_user.id
    message = f"Сотрудник с telegram id {tel_id} нажал кнопку: {answer}"
    context.bot.send_message(chat_id=MANAGER_CHAT_ID, text=message)


updater = Updater(TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("reminder", set_reminder))
dispatcher.add_handler(CallbackQueryHandler(button_click))

# Запуск
updater.start_polling()
