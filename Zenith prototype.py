import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
1
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    else:
        speak("Good evening!")

    speak("I am Jarvis Sir. Please tell me how may I help you")

def takeCommand():
    # it takes microphone input from the user and returns string output

    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('nimish1942@gmail.com', 'Nimish200342')
    server.sendmail('nimish1942@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
    #if 1:
        query = takeCommand().lower()
        
        #logic for executing query
        if 'information' in query:
            speak('Searching...')
            query = query.replace("information", "")
            results = wikipedia.summary(query, sentences=2)
            speak("Acocording to my knowledge")
            speak(results)
            print(results)

        elif 'open youtube' in query:
            webbrowser.open("www.youtube.com")

        elif 'open google' in query:
            webbrowser.open("www.google.com")

        elif 'open cloud computing textbook' in query:
            path= "E:\\cloud computing"
            os.startfile(path)

        elif 'open cloud platform' in query:
            webbrowser.open("www.cloud.google.com")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'email to nimish' in query:
            try:
                speak("what should I say")
                content = takeCommand()
                to = "nimish1942@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("sorry i cant send the mail at the moment")
        elif 'open gpt  ai' in query:
            webbrowser.open("chatgpt.com")
        
        elif 'open canva' in query:
            webbrowser.open("www.canva.com")

        elif 'open eid' in query:
            webbrowser.open("www.gmail.com")
            
        elif 'open netflix' in query:
            webbrowser.open("www.netflix.com")

        elif 'open brave private' in query:
            webbrowser.open("www.brave.com/npv")
        
        elif 'play music' in query:
            music_dir= 'N:\\music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        
