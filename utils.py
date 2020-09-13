import os
import subprocess
import uuid
from dataclasses import dataclass
from typing import List, Optional
from word_to_number.extractor import NumberExtractor
from telegram import Voice
from voicekit.library_voicekit import stt_wav_to_string, tts_string_to_wav

SEND_VOICE = True


@dataclass
class AnswerOption:
    number: int
    text: str
    is_correct: Optional[bool] = None
    id: Optional[str] = None


@dataclass
class Question:
    body: str
    answers: List[AnswerOption]
    right_text: str
    wrong_text: str


@dataclass
class CaseAction:
    is_up: bool
    amount: int


@dataclass
class Case:
    body: str
    outcomes: List[CaseAction]
    choices: List[AnswerOption]


@dataclass
class Domains:
    body: str
    choices: List[AnswerOption]


class TempFiles:
    def __init__(self, *extensions):
        self.extensions = extensions

    def __enter__(self):
        tmp_name = str(uuid.uuid4())
        self._files = [tmp_name + ext for ext in self.extensions]
        return self._files

    def __exit__(self, *args):
        for file in self._files:
            os.remove(file)


def _convert_audio(file_input, file_output):
    process = subprocess.run(["ffmpeg", "-i", file_input, file_output])
    if process.returncode != 0:
        raise Exception("Can not convert audio!")


def message_to_text(update, context, send_back_voice=True):
    if update.message.voice:
        with TempFiles(".ogg", ".wav") as (tmp_ogg, tmp_wav):
            voice_obj = update.message.voice
            voice_file = Voice(voice_obj.file_id, voice_obj.file_unique_id, voice_obj.duration, bot=context.bot)
            voice_file.get_file(timeout=100).download(tmp_ogg)

            _convert_audio(tmp_ogg, tmp_wav)

            text = stt_wav_to_string(tmp_wav)

        if send_back_voice:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"\"{text}\"")

        return text

    return update.message.text


def send_text_as_voice(text, update, context):
    with TempFiles(".ogg", ".wav") as (tmp_ogg, tmp_wav):
        tts_string_to_wav(text, tmp_wav)
        _convert_audio(tmp_wav, tmp_ogg)

        with open(tmp_ogg, "rb") as voice_file:
            context.bot.send_voice(chat_id=update.effective_chat.id, voice=voice_file)


def send_message(text, update, context):
    if SEND_VOICE:
        send_text_as_voice(text, update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text)


def is_correct(user_answer_string, answer_options_list, no_answer_options=False):
    extractor = NumberExtractor()
    user_answer_string = extractor.replace_groups(user_answer_string).lower()
    if no_answer_options and not len(answer_options_list) == 1:
        raise ValueError("There's actuatlly answer options")
    number_answer = None
    text_answer = None
    for option in answer_options_list:
        option.text, option.number = option.text.lower(), str(option.number).lower()
        number_answer = option if not no_answer_options and (option.number in user_answer_string.split(" ")) else number_answer
        if (option.text in user_answer_string) or (user_answer_string.isnumeric() and user_answer_string in option.text):
            text_answer = option

    user_answer = number_answer if number_answer else text_answer
    if not user_answer:
        result = False if no_answer_options else None
        return result
    result = user_answer.is_correct
    return result


def get_answered_option(user_answer_string, answer_options_list):
    extractor = NumberExtractor()
    user_answer_string = extractor.replace_groups(user_answer_string).lower()
    number_answer = None
    text_answer = None
    for option in answer_options_list:
        option.text, option.number = option.text.lower(), str(option.number).lower()
        number_answer = option if option.number in user_answer_string.split(" ") else number_answer
        if (option.text in user_answer_string) or (user_answer_string.isnumeric() and user_answer_string in option.text):
            text_answer = option

    user_answer = number_answer if number_answer else text_answer
    return user_answer


def has_more_questions(update, context):
    return True

# Test
if __name__ == "__main__":
    options = [AnswerOption("1", "25 лет", True), AnswerOption("2", "50 лет", False), AnswerOption("3", "6 лет", False), AnswerOption("4", "17 лет", False)]
    print(is_correct("семнадцать", options))
