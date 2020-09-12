import states
import texts
import handlers
from telegram.ext import MessageHandler, CommandHandler, Filters

domain_to_name = {
    "nails": "маникюрный салон"
}


def choose_domain_state_callback(update, context):
    # context.bot.send_message(chat_id=update.message.chat_id, text=texts.common.FAILED_TO_PARSE)
    domain = "nails"
    context.user_data["company_domain"] = domain
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=texts.onboarding.CHOSE_DOMAIN.format(domain=domain_to_name[domain]))
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=texts.onboarding.CHOOSE_NAME_PROMPT)
    return states.ONBOARDING_CHOOSE_NAME_STATE


def choose_name_state_callback(update, context):
    company_name = update.message.text
    context.user_data["company_name"] = company_name
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=texts.onboarding.CHOSE_NAME.format(name=company_name))
    # handlers.question.send_question(update, context)
    return states.QUESTION_MULTIPLE_CHOICE_STATE


choose_domain_state_handler = MessageHandler(Filters.all, choose_domain_state_callback)
choose_name_state_handler = MessageHandler(Filters.all, choose_name_state_callback)

states_to_handlers = {
    states.ONBOARDING_CHOOSE_DOMAIN_STATE: [choose_domain_state_handler],
    states.ONBOARDING_CHOOSE_NAME_STATE: [choose_name_state_handler],
}