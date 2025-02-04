import sqlite3
import eel
import os
import re
import webbrowser
import pywhatkit as kit
import pvporcupine
import time
import pyaudio
import struct
from playsound import playsound
from engine.config import ASSISTANT_NAME
from engine.command import speak
from engine.helper import extract_yt_term



con = sqlite3.connect("helena.db")
cursor = con.cursor()

#Playing Assistant initiation sound

@eel.expose
def playAssistantSound():
    music_dir = "www\\Assets\\audio\\Activation.mp3"
    playsound(music_dir)


@eel.expose
def playSiriSound():
    music_dir = "www\\Assets\\audio\\MicSound.mp3"
    playsound(music_dir)



def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("abrir", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Abrindo "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Abrindo "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Abrindo "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("Não encontrei")
        except:
            speak("Eita, algo deu errado")

#Youtube Follow up

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    a = "Reproduzindo "
    b = " no Youtube"
    speak(f"Reproduzindo {search_term} no YouTube")
    kit.playonyt(search_term)

def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("c")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()