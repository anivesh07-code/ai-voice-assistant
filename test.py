import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source, timeout=10)
    
# Save audio to file so we can hear what mic captured
with open("test.wav", "wb") as f:
    f.write(audio.get_wav_data())
    
print("Audio saved as test.wav - play it to check if mic is recording correctly")