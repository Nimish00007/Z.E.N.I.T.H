import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import whisper
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize text-to-speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

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
    speak("I am Jarvis Sir. Please tell me how may I help you")

def takeCommand():
    # Use SpeechRecognition for fast commands
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening (fast)...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception:
        print("Say that again please...")
        return "None"
    return query

def record_audio_whisper(filename="input.wav"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening (Whisper)...")
        audio = r.listen(source)
        with open(filename, "wb") as f:
            f.write(audio.get_wav_data())
    return filename

def transcribe_with_whisper(filepath="input.wav"):
    model = whisper.load_model("base")
    result = model.transcribe(filepath)
    print(f"Whisper heard: {result['text']}")
    return result["text"]

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('nimish1942@gmail.com', 'Nimish200342')  # 🔒 Move this to .env in production
    server.sendmail('nimish1942@gmail.com', to, content)
    server.close()

def interpret_with_ai(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or gpt-4
            messages=[
                {"role": "system", "content": "You are Jarvis, an AI assistant."},
                {"role": "user", "content": query}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return reply
    except Exception as e:
        print("AI Error:", e)
        return "Sorry, I'm having trouble understanding that."

if __name__ == "__main__":
    wishMe()
    while True:
        speak("Say your command, or say 'AI mode' to activate smart assistant")
        query = takeCommand().lower()

        if 'ai mode' in query:
            audio_file = record_audio_whisper()
            user_query = transcribe_with_whisper(audio_file)
            if user_query.lower() in ['exit', 'quit', 'stop']:
                speak("Goodbye, Sir!")
                break
            ai_reply = interpret_with_ai(user_query)
            speak(ai_reply)
            continue

        # Fallback to static commands
        if 'information' in query:
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
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I can't send the email at the moment")

        elif 'open gpt ai' in query:
            webbrowser.open("https://chatgpt.com")

        elif 'open canva' in query:
            webbrowser.open("https://www.canva.com")

        elif 'open eid' in query:
            webbrowser.open("https://www.gmail.com")

        elif 'open netflix' in query:
            webbrowser.open("https://www.netflix.com")

        elif 'open brave private' in query:
            webbrowser.open("https://www.brave.com/npv")

        elif 'play music' in query:
            music_dir = 'N:\\music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'exit' in query or 'quit' in query:
            speak("Goodbye Sir!")
            break
