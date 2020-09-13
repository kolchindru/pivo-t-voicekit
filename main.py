import os
import logging

from telegram.ext import Updater, PicklePersistence, CommandHandler, ConversationHandler, MessageHandler, Filters

import handlers
import states
import texts
import data

from utils import send_message

BOT_TOKEN = os.environ["BOT_API_KEY"]

persistence = PicklePersistence(filename='persistence.pickle')
updater = Updater(token=BOT_TOKEN, use_context=True, persistence=persistence)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - [%(name)s] - %(levelname)s: %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)


def start_callback(update, context):
    body_text = data.companies.body
    answers_text = "\n".join(f"{letter}. {answer}" for letter, answer in
                             zip(handlers.question.answer_numbers, [a.text for a in data.companies.choices]))
    text = f"{body_text}\n\n{answers_text}\n\nТы всегда можешь начать всё сначала, отправив команду /reset"
    send_message(text, update, context)
    return states.ONBOARDING_CHOOSE_DOMAIN_STATE


def reset_callback(update, context):
    return start_callback(update, context)


def unknown_callback(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=texts.common.FAILED_TO_PARSE)
    return


states_to_handlers = {
    **handlers.onboarding.states_to_handlers,
    **handlers.question.states_to_handlers,
    **handlers.decision.states_to_handlers,
}

start_handler = CommandHandler("start", start_callback)
reset_handler = CommandHandler("reset", reset_callback)
unknown_handler = MessageHandler(Filters.all, unknown_callback)
conversation_handler = ConversationHandler([start_handler, reset_handler], states_to_handlers, [reset_handler, unknown_handler])

dispatcher.add_handler(conversation_handler)

logger.info("Starting the bot.")
updater.start_polling()
