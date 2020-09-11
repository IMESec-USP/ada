from itertools import islice
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
import re
import logging

from .logger import Logger

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


class Handlers:

    @staticmethod
    def start(update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text=f'Olá, sou a Ada. O ID dessa conversa é {update.message.chat_id}. Se você é o administrador da Ada, sabe o que fazer.')

    @staticmethod
    def test(update, context):
        button = InlineKeyboardButton('Deploy', callback_data='Test 123')
        keyboard = InlineKeyboardMarkup.from_button(button)
        bot = context.bot
        bot.send_message(chat_id=update.message.chat_id, text='Isso é um teste de botão.', reply_markup=keyboard)


def callback_handler(update, context):
    bot = context.bot
    query = update.callback_query
    print('original message:', query.message.text)

    bot.answer_callback_query(query.id, text='Deployed!')
    bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text='Deployed!')

class TelegramHandler:

    SLICE_LENGTH = 4096

    def __init__(self, logger: Logger, api_token: str, conversations: dict):
        self.updater = Updater(api_token, use_context=True)
        self.conversations = conversations
        self.logger = logger.with_class_name(self)

        # reflection, baby
        handlers = [func for func in dir(Handlers) if callable(getattr(Handlers, func)) and not func.startswith("_")]
        self.logger.log(f'Adding command handlers for methods {handlers}')
        for handler_name in handlers:
            self.updater.dispatcher.add_handler(CommandHandler(handler_name, getattr(Handlers, handler_name)))

        self.updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))

    def poll(self):
        self.logger.log('Started polling telegram')
        self.updater.start_polling()

    def broadcast(self, message, filter_str='', sticker=None):
        bot = self.updater.bot

        conversations = []
        for conversation, filter_regex in self.conversations.items():
            if filter_str == '' or re.match(filter_regex, filter_str):
                conversations.append(conversation)
        self.logger.log(f'broadcasting message in conversations {conversations}')

        for chunk in self.chunks(message):
            for conversation in conversations:
                bot.send_chat_action(chat_id=conversation, action=ChatAction.TYPING)
                bot.send_message(chat_id=conversation, text=chunk)
                if sticker: bot.send_sticker(chat_id=conversation, text=chunk, sticker=sticker)

    @classmethod
    def chunks(cls, message):
        n = cls.SLICE_LENGTH
        it = iter(message)
        while True:
            chunk = ''.join(islice(it, n))
            if not chunk:
                return
            yield chunk
