import pyttsx3
import speech_recognition as sr
import eel
import time


def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 190)
    eel.DisplayMessage(text)
    engine.say(text)
    engine.runAndWait()


@eel.expose
def takecomand():

    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print('Estou te ouvindo...')
        eel.DisplayMessage('Estou te ouvindo...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)
    
    try:
        print('Reconhecendo')
        eel.DisplayMessage('Reconhecendo...')
        query = r.recognize_google(audio, language='pt-br')
        print(f"Voce disse: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        eel.ShowHood()
    except Exception as e:
        return ""
    

    return query.lower()

@eel.expose
def allComands():

    query = takecomand()
    print(query)

    if "abrir" in query:
        print ("Em processamento")
        from engine.features import openCommand
        openCommand(query)
    elif "no youtube":
        from engine.features import PlayYoutube
        PlayYoutube(query)

    else:
        print ("Não processado")

    eel.ShowHood()
