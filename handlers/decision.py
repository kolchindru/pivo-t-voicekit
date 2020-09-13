import states
import texts
import handlers
import random
from telegram.ext import MessageHandler, CommandHandler, Filters

import texts
import utils


def choose_company_action_callback(update, context):
    case = context.user_data["current_case"]
    answer_num = int(utils.get_answered_option(utils.message_to_text(update, context), case.choices).number) - 1
    context.user_data["company_price"] = context.user_data.get("company_price", 0) + case.outcomes[answer_num].amount
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=texts.common.RESPONSE_TO_DECISION.format(
                                 name=context.user_data["company_name"],
                                 number=case.outcomes[answer_num].amount,
                                 price=context.user_data["company_price"],
                             ))
    if utils.has_more_questions(update, context):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=texts.question.HAS_MORE_QUESTIONS)
        state = handlers.question.send_question(update, context)
        return state
    else:
        return states.NO_MORE_QUESTIONS_STATE


choose_company_action_handler = MessageHandler(Filters.text & (~Filters.command) | Filters.voice, choose_company_action_callback)

states_to_handlers = {
    states.DECISION_CHOICE_STATE: [choose_company_action_handler],
}
