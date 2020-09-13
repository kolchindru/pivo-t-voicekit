import random

from telegram.ext import MessageHandler, Filters

import utils
import data
import states
import texts

from utils import send_message

answer_numbers = "12345"


def send_question(update, context):
    question_type = random.choice(["free", "multiple"])
    if question_type == "free":
        current_question = random.choice(data.free_answer_questions)
        context.user_data["current_question"] = current_question
        text = current_question.body
        send_message(text, update, context)
        return states.QUESTION_FREE_CHOICE_STATE
    else:
        current_question = random.choice(data.multiple_choice_questions)
        context.user_data["current_question"] = current_question
        body_text = current_question.body
        answers_text = "\n".join(f"{letter}. {answer}" for letter, answer in
                                 zip(answer_numbers, [a.text for a in current_question.answers]))
        text = f"{body_text}\n{answers_text}"
        send_message(text, update, context)
        return states.QUESTION_MULTIPLE_CHOICE_STATE


def handle_question_answer(update, context, is_free_choice):
    current_question = context.user_data["current_question"]
    is_correct = utils.is_correct(update.message.text, current_question.answers,
                                  no_answer_options=is_free_choice)
    if is_correct is None:
        send_message(texts.common.FAILED_TO_PARSE, update, context)
        return
    if is_correct:
        context.bot.send_message(current_question.right_text, update, context)
        case = random.choice(data.cases)
        context.user_data["current_case"] = case

        body_text = case.body
        answers_text = "\n".join(f"{letter}. {answer}" for letter, answer in
                                 zip(answer_numbers, [a.text for a in case.choices]))
        text = f"{body_text}\n{answers_text}\nЧто ты выберешь?"
        send_message(text, update, context)
        return states.DECISION_CHOICE_STATE
    else:
        send_message(current_question.wrong_text, update, context)
        if utils.has_more_questions(update, context):
            send_message(texts.question.HAS_MORE_QUESTIONS, update, context)
            state = send_question(update, context)
            return state
        else:
            return states.NO_MORE_QUESTIONS_STATE


def free_choice_state_callback(update, context):
    return handle_question_answer(update, context, is_free_choice=True)


def multiple_choice_state_callback(update, context):
    return handle_question_answer(update, context, is_free_choice=False)


multiple_choice_state_handler = MessageHandler(Filters.text & (~Filters.command) | Filters.voice, multiple_choice_state_callback)
free_choice_state_handler = MessageHandler(Filters.text & (~Filters.command) | Filters.voice, free_choice_state_callback)

states_to_handlers = {
    states.QUESTION_MULTIPLE_CHOICE_STATE: [multiple_choice_state_handler],
    states.QUESTION_FREE_CHOICE_STATE: [free_choice_state_handler],
}