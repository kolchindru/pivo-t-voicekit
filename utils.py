import os
import subprocess
import uuid
from dataclasses import dataclass
from typing import List
from word_to_number.extractor import NumberExtractor
from telegram import Voice
from voicekit.library_voicekit import stt_wav_to_string, tts_string_to_wav


@dataclass
class AnswerOption:
    number: int
    text: str
    is_correct: bool


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
    choices: List[CaseAction]


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


def is_correct(user_answer_string, answer_options_list, no_answer_options=False):
    extractor = NumberExtractor()
    user_answer_string = extractor.replace_groups(user_answer_string)
    if no_answer_options and not len(answer_options_list) == 1:
        raise ValueError("There's actuatlly answer options")
    number_answer = None
    text_answer = None
    for option in answer_options_list:
        option.text, option.number = option.text.lower(), str(option.number).lower()
        number_answer = option if option.number in user_answer_string else number_answer
        text_answer = option if option.text in user_answer_string else text_answer

    user_answer = number_answer if number_answer else text_answer
    if not user_answer:
        result = False if no_answer_options else None
        return result
    result = user_answer.is_correct
    return result


# Test
options = [AnswerOption("1", "пиздато", False), AnswerOption("2", "хуёво", False), AnswerOption("3", "полный пиздец 1488", True)]
print(is_correct("вариант третий хуёво", options))