import states
import texts
import handlers
import random
from telegram.ext import MessageHandler, CommandHandler, Filters

import texts
import utils

from utils import send_message


def choose_company_action_callback(update, context):
    case = context.user_data["current_case"]
    answered_option = utils.get_answered_option(utils.message_to_text(update, context), case.choices)
    if answered_option is None:
        send_message(texts.common.FAILED_TO_PARSE, update, context)
        return
    answer_num = int(answered_option.number) - 1
    context.user_data["company_price"] = context.user_data.get("company_price", 0) + case.outcomes[answer_num].amount

    send_message(
        texts.common.RESPONSE_TO_DECISION.format(
             name=context.user_data["company_name"],
             number=case.outcomes[answer_num].amount,
             price=context.user_data["company_price"],
         ),
        update,
        context
    )
    if utils.has_more_questions(update, context):
        send_message(texts.question.HAS_MORE_QUESTIONS, update, context)
        state = handlers.question.send_question(update, context)
        return state
    else:
        return states.NO_MORE_QUESTIONS_STATE


choose_company_action_handler = MessageHandler(Filters.text & (~Filters.command) | Filters.voice, choose_company_action_callback)

states_to_handlers = {
    states.DECISION_CHOICE_STATE: [choose_company_action_handler],
}
