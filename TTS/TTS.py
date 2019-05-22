
def Txt2Voice(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

#Txt2Voice("hello")

