import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes

# Import additional libraries for OpenAI API
import requests
import json

# Define OpenAI API key
openai_key = "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"

# Set up SpeechRecognizer
listener = sr.Recognizer()

# Set up text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Function to speak text
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen for and recognize speech commands
def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            print(command)
    except:
        pass
    return command

# Function to answer questions using OpenAI API
def answer_question(question):
    # Set up OpenAI API request
    request_data = {
        "prompt": question,
        "length": 50
    }
    headers = {"Authorization": "Bearer " + openai_key}
    response = requests.post("https://api.openai.com/v1/engines/davinci/completions", json=request_data, headers=headers)
    response_data = response.json()
    # Get answer from response data
    answer = response_data["choices"][0]["text"]
    # Return answer
    return answer

# Function to run the Alexa skill
def run_alexa(command):
    # If command is a question, answer it
    if 'who' in command or 'what' in command or 'when' in command or 'where' in command or 'why' in command or 'how' in command:
        if 'why' in command:
            command = command.replace('why', '')
        answer = answer_question(command)
        talk(answer)
    # If command is not a question, respond normally
    else:
        if 'play' in command:
            song = command.replace('play', '')
            talk('playing ' + song)
            pywhatkit.playonyt(song)
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I%M %p')
            talk('Current time is ' + time)
        elif 'who is' in command:
            person = command.replace('who is', '')
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        elif 'date' in command:
            date = datetime.datetime.now().strftime('%B %d, %Y')
            talk('Current date is ' + date)
        elif 'are you single' in command:
            talk('I am in a relationship with wifi')
        elif 'joke' in command:
            talk(pyjokes.get_joke())
        else:
            talk('please say the command again')

# Run Alexa skill
while True:
    command_type = input("Enter 't' for text command or 'v' for voice command: ")
    if command_type == 'v':
        run_alexa(take_command())
    elif command_type == 't':
        command = input("Enter your command: ")
        run_alexa(command)

