import os
import subprocess
import uuid
from dataclasses import dataclass
from typing import List
from word_to_number.extractor import NumberExtractor
from telegram import Voice
from voicekit.library_voicekit import stt_wav_to_string


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


@dataclass
class AnswerOption:
    number: str
    text: str
    is_correct: bool


@dataclass
class CaseAction:
    is_up: bool
    amount: int


@dataclass
class Case:
    body: str
    choices: List[CaseAction]


def is_correct(user_answer_string, answer_options_list, no_answer_options=False):
    extractor = NumberExtractor()
    user_answer_string = extractor.replace_groups(user_answer_string)
    if no_answer_options and not len(answer_options_list) == 1:
        raise ValueError("There's actuatlly answer options")
    number_answer = None
    text_answer = None
    for option in answer_options_list:
        option.text, option.number = option.text.lower(), option.number.lower()
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
