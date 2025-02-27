# speech.py
import os
import speech_recognition as sr
from pydub import AudioSegment

def recognize_voice(bot, message):
    file_info = bot.get_file(message.voice.file_id)
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)

    audio_dir = "data"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    audio_ogg = os.path.join(audio_dir, "voice.ogg")
    audio_wav = os.path.join(audio_dir, "voice.wav")

    # 1. Сохраняем файл из Telegram в .ogg
    with open(audio_ogg, "wb") as f:
        f.write(downloaded_file)

    # 2. Конвертируем OGG -> WAV с помощью pydub
    try:
        track = AudioSegment.from_file(audio_ogg, format="ogg")
        track.export(audio_wav, format="wav")
    except Exception as e:
        print("Ошибка при конвертации аудио:", e)
        return None

    # 3. Распознаем речь из WAV
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_wav) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ru-RU")
            return text
        except sr.UnknownValueError:
            return None
