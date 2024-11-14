from playsound import playsound
import eel


#Playing Assistant initiaon sound

@eel.expose
def playAssistantSound():
    music_dir = "www\\Assets\\audio\\Activation.mp3"
    playsound(music_dir)
