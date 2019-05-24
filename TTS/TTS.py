import pyttsx3

engine = pyttsx3.init()

def Txt2Voice(text):
    engine.say(text)
    engine.runAndWait()

#Txt2Voice("hello")

