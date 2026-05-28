import speech_recognition as sr
import os
import datetime
import pyjokes
import subprocess
import shlex

recognizer = sr.Recognizer()

def speak(text: str):
    clean = text.replace('"', '').replace("'", '').replace('\n', ' ')
    print("Friday:", clean)
    subprocess.run(["say", clean])  # safer than os.system

def ai_response(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout.strip() or "I didn't get a response."
    except subprocess.TimeoutExpired:
        return "The AI took too long to respond."
    except Exception as e:
        return f"Error contacting AI: {e}"

def listen() -> str:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=5)
        return recognizer.recognize_google(audio).lower()
    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        print("Couldn't understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return ""

def open_url(url: str):
    subprocess.run(["open", url])  # macOS; use "xdg-open" on Linux

def processcommand(c: str) -> bool:
    """Returns False if the assistant should shut down."""
    print(f"Command: {c}")

    if "open youtube" in c:
        speak("Opening YouTube")
        open_url("https://www.youtube.com")
    elif "open google" in c:
        speak("Opening Google")
        open_url("https://www.google.com")
    elif "open instagram" in c:
        speak("Opening Instagram")
        open_url("https://www.instagram.com")
    elif "open gmail" in c:
        speak("Opening Gmail")
        open_url("https://mail.google.com")
    elif "time" in c:
        time_str = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time_str}")
    elif "date" in c:
        date_str = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {date_str}")
    elif "joke" in c:
        speak(pyjokes.get_joke())
    elif "wikipedia" in c:
        topic = c.replace("wikipedia", "").strip()
        speak(f"Opening Wikipedia for {topic}")
        open_url(f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}")
    elif "play" in c:
        song = c.replace("play", "").strip()
        speak(f"Playing {song}")
        open_url(f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}")
    elif "weather" in c:
        speak("Opening weather")
        open_url("https://www.weather.com")
    elif "exit" in c or "stop" in c:
        speak("Shutting down. Goodbye.")
        return False  # signal to exit loop
    else:
        speak("Let me think about that.")
        reply = ai_response(c)
        print("AI:", reply)
        speak(reply)

    return True

if __name__ == "__main__":
    speak("Initializing Friday. Say my name to wake me up.")
    while True:
        text = listen()
        if "friday" in text:
            speak("Yes?")
            command = listen()
            if command:
                should_continue = processcommand(command)
                if not should_continue:
                    break