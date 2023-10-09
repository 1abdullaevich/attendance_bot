#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from helpers import *

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    # keyboard = [
    #     [
    #         InlineKeyboardButton("Option 1", callback_data="1"),
    #         InlineKeyboardButton("Option 2", callback_data="2"),
    #     ],
    #     [InlineKeyboardButton("Option 3", callback_data="3")],
    # ]
    keyboard = []
    data = get_groups()
    for group in data:
        temp = [InlineKeyboardButton(group["name"], callback_data=f'group-{group["id"]}')]
        keyboard.append(temp)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    answer = query.data
    answer_splitted = answer.split('-')
    if answer_splitted[0] == 'group':
        students = start_attendance(answer_splitted[1])
        keyboard = []
        for student in students:
            print(student)
            sign = "✔️"
            if student["is_come"] == False:
                sign = "❌"
            temp = [InlineKeyboardButton(f'{student["student_full_name"]} {sign}',
                                         callback_data=f'student-{student["id"]}')]
            keyboard.append(temp)
        keyboard.append([InlineKeyboardButton(
            "<== Back", callback_data='back'
        )])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f'Selected option:', reply_markup=reply_markup)

    elif answer_splitted[0] == 'back':
        keyboard = []
        data = get_groups()
        for group in data:
            temp = [
                InlineKeyboardButton(group["name"], callback_data=f'group-{group["id"]}')
            ]
            keyboard.append(temp)

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("Please choose:", reply_markup=reply_markup)

    elif answer_splitted[0] == 'student':
        students = change_status(answer_splitted[1])
        keyboard = []
        for student in students:
            print(student)
            sign = "✔️"
            if student["is_come"] == False:
                sign = "❌"
            temp = [InlineKeyboardButton(f'{student["student_full_name"]} {sign}',
                                         callback_data=f'student-{student["id"]}')]
            keyboard.append(temp)
        keyboard.append([InlineKeyboardButton(
            "<== Back", callback_data='back'
        )])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=f'Selected option:', reply_markup=reply_markup)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6481428939:AAHlIykoUFecjF7dQvP6SFL3VuqzihS8Je8").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button))

    # on non command i.e message - echo the message on Telegram
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
