import os
#import text to speech library
from google.cloud import texttospeech as MAIVA
#to play the mp3 files
from playsound import playsound as maiva_say
import time
import speech_recognition as sr
from datetime import date
import random
import json

#initialise MAIVA engine
maiva_engine = MAIVA.TextToSpeechClient()
#give MAIVA a voice
maiva_voice = MAIVA.VoiceSelectionParams(language_code='en-GB', name="en-GB-Wavenet-F" , ssml_gender=MAIVA.SsmlVoiceGender.FEMALE)
#set up audio configurations
maiva_audio_config = MAIVA.AudioConfig(audio_encoding=MAIVA.AudioEncoding.MP3)

#needed global variables
global system_alive 
global wake_word
global client_name 


#variable initialisation 
system_alive = False
client_name =  "."
wake_word = "computer"
auto_google = "google"
voice_recognition = sr.Recognizer()
mic = sr.Microphone()
legible = False




#### ======= TO DO ======== ####

'''need to add a file of all possible commands to respond to'''


'''need to interface with spotify AI'''


'''add generic google search feature'''


'''current weather readout'''


'''calendar events'''

#### ======= TO DO ======== ####




#MAIVA initialisation sequence
def main():
    print ("Initialising MAIVA....")
    #set lower threshold for better recognition
    time.sleep(1)
    #introduce MAIVAs availability 
    speak("Boot sequence complete")
    time.sleep(1)    
    print("MAIVA online.")
    toggle_system_life(True)
    listen()

    

#MAIVA vocal function
def speak(output_phrase):
    #save response
    print ("Generating response...")
    #convert text phrase into synthesis input
    phrase_input = MAIVA.SynthesisInput(text=output_phrase)
    #maiva engine synthesises spoken response
    maiva_response = maiva_engine.synthesize_speech(input=phrase_input, voice=maiva_voice, audio_config=maiva_audio_config)
    save(maiva_response)
    maiva_say('./resources/maiva_response')
   
    
    
def listen():
    global wake_word

    #MAIVA continuously polls for wake word in a sentence
    while system_alive == True: 
        with mic as source:
            voice_recognition.adjust_for_ambient_noise(source)
            voice_recognition.energy_threshold = 4000

            audio = voice_recognition.listen(source)
            try:
                command = voice_recognition.recognize_google(audio, language="en-GB")
                print("MAIVA is thinking about your request...")
                time.sleep(1)
                
                legible = True
            except:
                legible = False
                
            if legible:
                #check if the legible sentence contains the wake word
                if (wake_word.lower() in command.lower()) or(auto_google in command.lower()):
                    #send command to MAIVAs brain
                    print("Request: " + str(command))
                    brain(command)
                else:
                    print("I can't understand that, sorry.")
    
    print("It was nice being real.")
    
    
    
def question_reply():
    
    #used to specifically listen for a reply to a MAIVA question outside main program loop!
    
    pass
    
    
    
    
#process legible command    
def brain(command):
    
    ##could have a list of opening remarks to randomly choose from or skip here
    #makes the system seem more intuitive
    speak("Let me see")
    
    #ensure access to the correct variable
    global client_name
    global wake_word
    
    #date query
    if ("the date" in command) or ("what's the date" in command) or ("today's date" in command):
        speak("The date today is " + str(date.today()))
    elif ("power down" in command) or ("shut down" in command) or ("power off" in command) or ("die " + str(wake_word) + "" in command):
        toggle_system_life(False)
        speak("Certainly")
    elif("what's my name" in command) or ("what is my name" in command) or ("tell me my name" in command):
        if client_name == ".":
            speak("You haven't told me your name yet")
        else:
            speak("You've asked me to call you " + str(client_name))
    elif("what's your name" in command) or ("what is your name" in command) or ("tell me your name" in command) or ("what are you called" in command):
        speak("My name is Mayva. I'm the mashka artificially intelligent voice assistant")
    elif("set my name to" in command) or ("my name is" in command) or ("set name as" in command) or ("you can call me" in command):
        words = command.split()
        temp_client_name = ""
        if(words[len(words) -1] == wake_word):
            temp_client_name = words[len(words) - 2]
        else:
            temp_client_name = words[len(words) - 1]
        if any(char.isdigit() for char in temp_client_name) == False:
            client_name = temp_client_name
            speak("I'll call you " + str(client_name) + " then")
        else:
            speak("I had difficulty understanding that")        
    elif("set wake word to" in command) or ("wake up to" in command) or ("new wake word is" in command):
        words = command.split()
        if(words[len(words) -1] == wake_word):
            temp_wake_word = words[len(words) - 2]
        else:
            temp_wake_word = words[len(words) - 1]

        if any(char.isdigit() for char in temp_wake_word) == False:
            wake_word = temp_wake_word
            speak ("New wake word set")
        else:
            speak("Wake word not possible")
    elif ("who is the king" in command) or ("like cera post" in command) or ("king" in command) or ("run cera liker" in command) or ("like michael cera's post" in command):
        speak("I'll sort that for you sir.")
        bashCommand = "python ../cera_liker.py"
        os.system(bashCommand)
    elif("something interesting" in command) or ("something cool" in command):
        #generate random number
        f = open('./resources/coolstuff.txt')
        interesting = ""
        lines = f.readlines()
        #ensure MAIVA responds with something
        while interesting == "":
            random_number = random.randint(0, 75)
            interesting = str(lines[random_number])
        speak(interesting)
    elif("something funny" in command) or ("tell me a joke" in command) or ("make me laugh" in command) or ("cheer me up" in command):
        #generate random number
        f = open('./resources/jokes.txt')
        joke = ""
        lines = f.readlines()
        #ensure MAIVA responds with something
        while True:

            #index outside bounds error needs looking at here
            random_number = random.randint(0, 15)
            joke = str(lines[random_number])
            if joke != "" and joke != " " and joke != "\n":
                break
        speak(joke)
    elif("tell me a fact" in command) or ("give me a fact" in command) or ("let's hear a fact" in command):
        #generate random number
        f = open('./resources/facts.txt')
        fact = ""
        lines = f.readlines()
        #ensure MAIVA responds with something
        while True:

            #index outside bounds error needs looking at here
            random_number = random.randint(0, 15)
            fact = str(lines[random_number])
            if fact != "" and fact != " " and fact != "\n":
                break
        speak(fact)
    else:
        speak("I'm not sure I understood you")
        
    
        
        
    
        
    

'''
Function to save the MAIVA response audio
so it can be pronounced by MAIVA
'''    
def save(maiva_response):
    f = open('./resources/maiva_response', 'wb')
    f.write(maiva_response.audio_content)
    f.close()



'''
Method used to boot MAIVA and shut MAIVA down
cleans the global variable access up
'''
def toggle_system_life(boolean):
    global system_alive
    system_alive = boolean



#spawn MAIVA
main()


