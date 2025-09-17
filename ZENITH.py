from voice_auth import authenticate
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import openai
from dotenv import load_dotenv
import google.generativeai as genai
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pickle

# Load environment variables
load_dotenv()
openai.api_key = my_api_key = "AIzaSyBNqgusPyVr0P_cl4tujS3e2rQL2bQveVs"
genai.configure(api_key=my_api_key)

# Initialize TTS
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    print(f"Jarvis: {audio}")
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Zenith Sir. Please tell me how may I help you")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.8
        r.energy_threshold = 300
        r.adjust_for_ambient_noise(source, duration=0.90)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        print("Say that again please...")
        return "None"
    return query

def sendEmail(creds, to, subject, body):
    try:
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEMultipart()
        message['to'] = to
        message['subject'] = subject
        msg = MIMEText(body)
        message.attach(msg)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
        print(f'Message sent: {send_message["id"]}')
        speak("Email has been sent!")
    except HttpError as error:
        print(f'An error occurred: {error}')
        speak("Sorry, I can't send the email at the moment.")

def load_credentials():
    creds = None
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        print("Credentials expired or invalid. Please authenticate again.")
    return creds

def start_jarvis():
    wishMe()
    creds = load_credentials()

    while True:
        speak("Say your command, or say 'AI mode' to activate smart assistant")
        query = takeCommand().lower()

        if 'ai mode' in query:
            speak("AI Mode activated. You can start speaking now. Say 'exit' to quit AI mode.")
            chat_model = genai.GenerativeModel('gemini-pro')
            chat_session = chat_model.start_chat(history=[])

            while True:
                speak("Listening in AI mode...")
                user_input = takeCommand()

                if user_input.lower() in ['stop','quit','exit']:
                    speak("Exiting AI mode. How else may I help you?")
                    break

                try:
                    response = chat_session.send_message(user_input)
                    reply = response.text
                    print("Gemini:", reply)
                    speak(reply)
                except Exception as e:
                    print("Gemini error:", e)
                    speak("Sorry, I'm facing an issue with Gemini right now.")

        elif 'information' in query:
            speak('Searching...')
            query = query.replace("information", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to my knowledge")
            speak(results)
            print(results)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'open cloud computing textbook' in query:
            path = "E:\\cloud computing"
            os.startfile(path)

        elif 'open cloud platform' in query:
            webbrowser.open("https://cloud.google.com")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'email to nimish' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "nimish1942@gmail.com"
                subject = "Subject: Jarvis Email"
                sendEmail(creds, to, subject, content)
            except Exception as e:
                print(e)
                speak("Sorry, I can't send the email at the moment.")

        elif 'open gpt ai' in query:
            webbrowser.open("https://chatgpt.com")

        elif 'open canva' in query:
            webbrowser.open("https://www.canva.com")

        elif 'open mail' in query:
            webbrowser.open("https://www.gmail.com")

        elif 'open netflix' in query:
            webbrowser.open("https://www.netflix.com")

        elif 'open brave' in query:
            webbrowser.open("https://www.brave.com/npv")

        elif 'play music' in query:
            music_dir = 'N:\\music'
            songs = os.listdir(music_dir)
            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No music files found.")

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye Sir!")
            break

if __name__ == "__main__":
    if authenticate("jarvis3.wav"):
        start_jarvis()
    else:
        print(" Voice authentication failed. Access denied.")
        speak("Voice authentication failed. Access denied.")
