import speech_recognition as sr
import pyttsx3
from datetime import datetime
import urllib.request
import webbrowser
import config
import wikipedia


# Opening a url
def open_url(url):
    web_url = urllib.request.urlopen(url)
    webbrowser.open(url)
    print("result: " + str(web_url.getcode()))


# Creating Listener
listener = sr.Recognizer()
# Added this after ALSA errors, ran $ python3 -m speech_recognition to get threshold
listener.energy_threshold = 1268
listener.dynamic_energy_threshold = True

# Creating voice engine
# Had to install librespeak1 to fix errors here
engine = pyttsx3.init()

# Making rosa female
voices = engine.getProperty('voices')
# Using espeak here to get a female voice
engine.setProperty('voice', 'english_rp+f3')


# Getting Rosa to talk
def rosa_talk(text):
    engine.say(text)
    engine.runAndWait()


# ran into few errors using the microphone, ALSA errors still appear but works anyway after adding energy_threshold^
# Had to install pyaudio, ran $ sudo apt install portaudio19-dev then installed
def get_command():
    try:
        with sr.Microphone() as source:
            print("I'm Listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice, language='en')
            command = command.lower()

            if 'rosa' in command:
                command = command.replace('rosa', '')
                print(command)
            else:
                print("Say my name")

    except Exception as e:
        return "No voice detected...."
    return command


# Running Rosa and executing commands
def run_rosa():
    rosa_talk('Hello, How can i help?')
    rosa_command = get_command()
    print(rosa_command)
    execute_commands(rosa_command)


# Executing commands
def execute_commands(command):
    # Telling time
    if 'time' in command:
        time = datetime.now().strftime("%d/%m/%Y")
        rosa_talk('The current time is ' + time)
    # Opening Uni stuff
    if 'uni' in command:
        open_url("https://canvas.qut.edu.au/")
    # Say a Lyric


run_rosa()

