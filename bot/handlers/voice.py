import speech_recognition as sr
from pathlib import Path
from dispatcher import bot
from aiogram import types
import os


async def download_voice(file: types.File , file_name: str, path: str) ->bool:
    Path(f"{path}").mkdir(parents=True, exist_ok=True)
    await bot.download_file(file_path=file.file_path, destination=f"{path}{file_name}")


async def transcibeVoice(voice, path):
    await download_voice(file=voice, file_name=f"{voice.file_id}.ogg", path=path)
    os.system(f"ffmpeg -i {path}{voice.file_id}.ogg {path}{voice.file_id}.wav")


#recognize wav file to text
async def recognize_voice(voice, language="ru-RU") -> str:
    path = "bot/download/voices/"
    await transcibeVoice(voice, path)
    try:
        r = sr.Recognizer()
        with sr.WavFile(f"{path}{voice.file_id}.wav") as source:
            #r.adjust_for_ambient_noise(source) # Optional
            audio = r.record(source)
        text = r.recognize_google(audio, language=language)
        os.remove(f'{path}{voice.file_id}.ogg')
        os.remove(f'{path}{voice.file_id}.wav')
        return text
    except sr.UnknownValueError:
        return "Ошибка распознавания."
    except sr.RequestError as e:
        return "Could not request results from Speech to Text service"