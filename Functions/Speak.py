import requests as rq
import colorama
import threading
import pygame
import base64
colorama.init(autoreset=True)
import sys
import os
current_dir=os.getcwd()
sys.path.append(current_dir)
from API_keys import AI_Name
from Functions.Hotword_Detection import hotword_detection
requests = rq.Session()


IS_HOT_WRD = False
HOT_WORD_DECT_IS_ON = False

url="https://deepgram.com/api/ttsAudioGeneration"

Sophia="aura-asteria-en"
Emily="aura-luna-en"
Kevin="aura-orion-en"
Jeff="aura-arcas-en"

def HOT_WORD_DECT():
    global IS_HOT_WRD, HOT_WORD_DECT_IS_ON
    while True:
        if HOT_WORD_DECT_IS_ON:
            A = hotword_detection()
            if A:
                if HOT_WORD_DECT_IS_ON:
                    IS_HOT_WRD = True
                    return
                else:
                    pass
        else:
            return

def file_saver(text, model):
    payload={
        'model': model,
        'text': text
    }
    response=requests.post(url, json=payload)
    with open('temp/data.mp3', 'wb')as f:
        f.write(base64.b64decode(response.json()['data']))

def speak(text, PRINT=True, MaleVoice=False):
    pygame.mixer.init()
    global IS_HOT_WRD, HOT_WORD_DECT_IS_ON
    HOT_WORD_DECT_IS_ON = True
    threading.Thread(target=HOT_WORD_DECT).start()
    if PRINT:
        print(colorama.Fore.YELLOW + f"==> {AI_Name} AI: " + text + "\n")
    if MaleVoice:
        file_saver(text,Jeff)
    else:
        file_saver(text,Emily)
    try:
        pygame.mixer.music.load(r"temp/data.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            if IS_HOT_WRD:
                IS_HOT_WRD = False
                pygame.mixer.music.stop()
                break
    except Exception as e:
        print(e)
    finally:
        pygame.mixer.quit()
        HOT_WORD_DECT_IS_ON = False

print("==> Speech Loaded!")

if __name__ == "__main__":
    while True:
        speak("Hello sir this is Jarvis in Brian's voice hi this is jarvis")
        speak("hi this is jarvis")
        speak("sir welcome")
        speak("welcome sir")