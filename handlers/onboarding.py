from telegram.ext import MessageHandler, CommandHandler, Filters

import utils
import data
import states
import texts
import handlers

from utils import send_message

domain_to_name = {
    "coffee": "эко-френдли кофейня",
    "nails": "маникюрный салон",
    "scooter": "сервис по аренде самокатов",
}


def choose_domain_state_callback(update, context):
    answered_option = utils.get_answered_option(utils.message_to_text(update, context), data.companies.choices)
    # context.bot.send_message(chat_id=update.message.chat_id, text=texts.common.FAILED_TO_PARSE)
    if answered_option is None:
        send_message(texts.common.FAILED_TO_PARSE, update, context)
        return
    domain = answered_option.id
    context.user_data["company_domain"] = domain
    send_message(texts.onboarding.CHOSE_DOMAIN.format(domain=domain_to_name[domain]), update, context)
    send_message(texts.onboarding.CHOOSE_NAME_PROMPT, update, context)
    return states.ONBOARDING_CHOOSE_NAME_STATE


def choose_name_state_callback(update, context):
    company_name = update.message.text
    context.user_data["company_name"] = company_name
    send_message(texts.onboarding.CHOSE_NAME.format(name=company_name), update, context)
    state = handlers.question.send_question(update, context)
    return state


choose_domain_state_handler = MessageHandler(Filters.text & (~Filters.command) | Filters.voice, choose_domain_state_callback)
choose_name_state_handler = MessageHandler(Filters.text & (~Filters.command) | Filters.voice, choose_name_state_callback)

states_to_handlers = {
    states.ONBOARDING_CHOOSE_DOMAIN_STATE: [choose_domain_state_handler],
    states.ONBOARDING_CHOOSE_NAME_STATE: [choose_name_state_handler],
}