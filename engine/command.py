import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 190)
    print(voices)
    engine.say(text)
    engine.runAndWait()


@eel.expose
def takecomand():

    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print('Estou te ouvindo...')
        eel.DisplayMessage('listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, 10, 6)
    
    try:
        print('Reconhecendo')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='pt-br')
        print(f"Voce disse: {query}")
        eel.DisplayMessage(query)
        speak(query)
        eel.ShowHood()
    except Exception as e:
        return ""
    

    return query.lower()


