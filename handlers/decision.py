import states
import texts
import handlers
import random
from telegram.ext import MessageHandler, CommandHandler, Filters

import texts
import utils


def choose_company_action_callback(update, context):
    case = context.user_data["current_case"]
    answer_num = utils.get_answered_option(utils.message_to_text(update, context), ["a", "b"]) - 1
    context.user_data["company_price"] = context.user_data.get("company_price", 0) + case.choices[answer_num]
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=texts.common.RESPONSE_TO_DECISION.format(context.user_data["company_price"]))

    return states.CHECK_QUESTIONS_LEFT_STATE


def check_questions_left_callback(update, context):
    if context.user_data.get("questions_left", 0) == 0:
        return states.NO_MORE_QUESTIONS_STATE
    return states.QUESTION_MULTIPLE_CHOICE_STATE


choose_company_action_handler = MessageHandler(Filters.all, choose_company_action_callback)
check_questions_left_handler = MessageHandler(Filters.all, check_questions_left_callback)

states_to_handlers = {
    states.DECISION_CHOICE_STATE: [choose_company_action_handler],
    states.CHECK_QUESTIONS_LEFT_STATE: [check_questions_left_handler]
}
