import speech_recognition as sr
import pyttsx3
from datetime import datetime
import urllib.request
import webbrowser
import config
import openai
import requests


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
                pass

    except Exception as e:
        rosa_talk("No voice detected..")
        return "placeholer"

    return command


# Using openai to respond
def openai_response(command):
    openai.api_key = config.openai_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": command},
        ]
    )

    result = ''
    for choice in response.choices:
        result += choice.message.content

    return result


# Using OpenWeatherMap API
def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?&q={city}&appid={config.openweathermap_key}&units=metric'
    response = requests.get(url)
    data = response.json()
    forcast = data['weather'][0]['description']
    temp = data['main']['temp']

    return f"The forcast for {city} is {str(forcast)} and the temperature is {str(temp)}"


# Executing commands
def execute_commands(command):
    # Telling time
    if 'date' in command:
        time = datetime.now().strftime("%d/%m/%Y")
        rosa_talk('The current date is ' + time)
    # Opening Uni stuff
    elif 'uni' in command:
        open_url("https://canvas.qut.edu.au/")
        rosa_talk('I have opened canvas')
    # Getting weather
    elif 'weather' in command:
        rosa_talk("What city?")
        city = get_command()
        rosa_talk(get_weather(city))

    elif 'what is your name' in command:
        rosa_talk("My name is Rosa")
    # Quitting rosa
    elif 'quit' in command:
        rosa_talk("Goodbye")
        return
    else:
        result = openai_response(command)
        rosa_talk(result)
        print(result)
    run_rosa()


# Running Rosa and executing commands
def run_rosa():
    rosa_command = get_command()
    print(rosa_command)
    execute_commands(rosa_command)


if __name__ == "__main__":
    rosa_talk("Hello, how can i help you today?")
    run_rosa()
