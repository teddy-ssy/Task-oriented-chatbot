import os
from SpeechRecogniztion.Constants import *
import speech_recognition as sr
import time


def Start_one_speech():

    print("please:")
    stop=True
    last="yes"
    while(stop):
        r = sr.Recognizer()
        with sr.Microphone()as source:
            audio = r.listen(source)
        try:
            if r.recognize_google(audio)== "yes":
                stop=False

            if stop==True:
                print("do you mean: " + r.recognize_google(audio))
                last=r.recognize_google(audio)
        except sr.UnknownValueError:
            print("waiting")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return last

#sentence = Start_one_speech()
#print(sentence)





