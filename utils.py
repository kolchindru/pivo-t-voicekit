import os
import subprocess
import uuid
from dataclasses import dataclass
from typing import List
from word_to_number.extractor import NumberExtractor
from telegram import Voice
from voicekit.library_voicekit import stt_wav_to_string


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


def message_to_text(update, context, send_back_voice=True):
    if update.message.voice:
        tmp_name = str(uuid.uuid4())
        tmp_ogg = tmp_name + ".ogg"
        tmp_wav = tmp_name + ".wav"

        voice_obj = update.message.voice
        voice_file = Voice(voice_obj.file_id, voice_obj.file_unique_id, voice_obj.duration, bot=context.bot)
        voice_file.get_file(timeout=100).download(tmp_ogg)

        process = subprocess.run(["ffmpeg", "-i", tmp_ogg, tmp_wav])
        if process.returncode != 0:
            raise Exception("Can not convert .ogg to .wav!")

        text = stt_wav_to_string(tmp_wav)

        if send_back_voice:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"\"{text}\"")

        os.remove(tmp_ogg)
        os.remove(tmp_wav)

        return text

    return update.message.text


def is_correct(user_answer_string: str, answer_options_list: List[AnswerOption], no_answer_options: bool = False):
    extractor = NumberExtractor()
    user_answer_string = extractor.replace_groups(user_answer_string)
    if no_answer_options and not len(answer_options_list) == 1:
        raise ValueError("There are actually answer options")
    user_answer = None
    for option in answer_options_list:
        option.text, option.number = option.text.lower(), str(option.number).lower()
        user_answer = option if (option.text in user_answer_string) or (option.number in user_answer_string) else user_answer
        if user_answer:
            break
    if not user_answer:
        result = False if no_answer_options else None
        return result
    result = user_answer.is_correct
    return result
