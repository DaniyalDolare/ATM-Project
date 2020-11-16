# Import the required module for text 
# to speech conversion 
from gtts import gTTS 

# This module is imported so that we can 
# play the converted audio 
import os 

# The text that you want to convert to audio 
mytext = 'Welcome to atm'

# Language in which you want to convert 
language = 'en'

# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed 
myobj = gTTS(text=mytext, lang=language, slow=False) 

# Saving the converted audio in a mp3 file named 
# welcome 
myobj.save("hey.mp3") 

# Playing the converted file 
os.system("mpg321 hey.mp3") 

"""
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')   
for voice in voices: 
    engine.setProperty('voice', voice.id)
    print(voice)
    #engine.setProperty('voice', voices[1].id)   
    engine.say("I will speak this text")
    engine.runAndWait()
"""
