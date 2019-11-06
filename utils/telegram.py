from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton

from itertools import islice
import logging
import threading
from functools import partial

from ada_ansible.redeploy_images import redeploy_images

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
    def in_thread():
        bot = context.bot
        query = update.callback_query
        edit_message = partial(bot.edit_message_text, chat_id=query.message.chat_id, message_id=query.message.message_id)

        edit_message(text='Fazendo update nas imagens necessarias...')
        bot.answer_callback_query(query.id, text='Fazendo deploy...')
        results = redeploy_images()
        if results is None:
            edit_message(text='Não consegui utilizar o Ansible no momento. Talvez alguém tenha apertado o botão antes de você em algum outro chat.')
            return

        edit_message(text='Deployed!')

    thread = threading.Thread(target=in_thread, args=tuple())
    thread.start()

class TelegramHandler:

    SLICE_LENGTH = 4096
    
    def __init__(self, api_token: str, conversations = list):
        self.updater = Updater(api_token, use_context=True)
        self.conversations = conversations

        # reflection, baby
        handlers = [func for func in dir(Handlers) if callable(getattr(Handlers, func)) and not func.startswith("_")]
        for handler_name in handlers:
            self.updater.dispatcher.add_handler(CommandHandler(handler_name, getattr(Handlers, handler_name)))

        self.updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
            
    def poll(self):
        self.updater.start_polling()

    def broadcast(self, message):
        bot = self.updater.bot
        for chunk in self.chunks(message):
            for conversation in self.conversations:
                bot.send_chat_action(chat_id=conversation, action=ChatAction.TYPING)
                bot.send_message(chat_id=conversation, text=chunk)
    
    def broadcast_deploy(self, message):
        pass

    @classmethod
    def chunks(cls, message):
        n = cls.SLICE_LENGTH
        it = iter(message)
        while True:
            chunk = ''.join(islice(it, n))
            if not chunk:
                return
            yield chunk