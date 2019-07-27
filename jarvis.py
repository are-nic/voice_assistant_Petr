# Голосовой ассистент

import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime

opts = {    # словарь ассистента
    'alias': ('чувак', 'просыпайся тварь', 'питон', 'петя', 'петр', 'Петр', 'питун', 'пётр'),
    # хранит в себе варианты имени при вызове помощника
    # to be removed - слова, которые будут удалены из речевой команды
    'tbr': ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    'cmds': {   # хранит все возможные команды, которые выполняет помощник
        'ctime': ('который час', 'сколько времени', 'текущее время'),
        'radio': ('включи музыку', 'включи радио')
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


# вызывается, когда записывает какую-либо фразу из микрофона, преобразовывает запись в текст
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language='ru-RU').lower()
        print('[log] Распознано: ' + voice)

        if voice.startswith(opts['alias']):     # если фраза началась с имени помощника,
            # вырезаем из полученного текста все возможные имена помощника и слова из словаря 'tbr'
            # остается чистый вариант внесенной команды
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознание и выпролнение команды
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print('[log] Голос не распознан!')
    except sr.RequestError:
        print('[log] Неизвестная ошибка, проверьте интернет!')


def recognize_cmd(cmd):             # нечетнкий поиск команд, которые получил помощник (библиотека fuzzywuzzy)
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC


def execute_cmd(cmd):               # для преобразования команды в действие
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak('Сейчас ' + str(now.hour) + ':' + str(now.minute))

    elif cmd == 'radio':
        # воспроизвести музыку
        os.startfile(r'C:\Users\Руслан\Music\30 Seconds to Mars - Love Lust Faith + Dreams - 2013 (320 kbps)\05. The Race.mp3')

    else:
        print('Команда не распознана, хозяин!')


# запуск ассистента
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)          # метод в течение 1 сек слушает фон чобы отделять шум от голоса

speak_engine = pyttsx3.init()

# Только если установлены голоса для синтеза речи (в стандартной винде 3 голоса) после voices в setProperty указать [4].id
voices = speak_engine.getProperty('voices')      # метод для указания голоса, которым будет говорить помощник
speak_engine.setProperty('voice', voices)

speak('Да, хозяин')


stop_listening = r.listen_in_background(m, callback)    # метод для прослушивания микрофона в фоне
while True:
    time.sleep(0.1)
