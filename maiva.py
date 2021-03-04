import os
#import text to speech library
from google.cloud import texttospeech as MAIVA
#to play the mp3 files
from playsound import playsound as maiva_say
import time
import speech_recognition as sr
from datetime import date
import datetime
import random
import subprocess
import threading
import sys
#from capabilities import tell_fact

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


'''play some x feature'''

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
                    print("Wake word not detected sorry")
    
    print("It was nice being real.")
    sys.exit(1)
    
    
    
def question_reply(keyword):
    pass
    #used to specifically listen for a reply to a MAIVA question outside main program loop!
    with mic as source:
        voice_recognition.adjust_for_ambient_noise(source)
        voice_recognition.energy_threshold = 4000

        audio = voice_recognition.listen(source)
        try:
            command = voice_recognition.recognize_google(audio, language="en-GB")
            legible = True
        except:
            legible = False
            
        if legible:
            #check if the legible sentence contains the wake word
            if (keyword in command.lower()):
                pass
    
    
#process legible command    
def brain(command):
    opening_remarks = open('./resources/opening_remarks.txt')
    opening_remarks_lines = opening_remarks.readlines()
    ##could have a list of opening remarks to randomly choose from or skip here
    #makes the system seem more intuitive
    random_int = random.randint(0, 2)

    #greeting to be used for more complex classes of replies
    greeting = str(opening_remarks_lines[random_int])
    opening_remarks.close()
    #ensure access to the correct variable
    global client_name
    global wake_word
    
  
  
  
    
    #date query
    if ("the date" in command) or ("what's the date" in command) or ("today's date" in command):
        speak(greeting)
        speak("The date today is " + str(date.today()))
    elif ("power down" in command) or ("shut down" in command) or ("power off" in command) or ("die " + str(wake_word) + "" in command) or ("shutdown" in command):
        toggle_system_life(False)
        speak("Certainly")
    elif("what's my name" in command) or ("what is my name" in command) or ("tell me my name" in command):
        if client_name == ".":
            speak("I wish I knew. Please tell me.")
        else:
            speak("You've asked me to call you " + str(client_name))
    elif("what's your name" in command) or ("what is your name" in command) or ("tell me your name" in command) or ("what are you called" in command):
        speak("My name is Mayva. I'm mashka the artificially intelligent voice assistant")
    elif("set my name to" in command) or ("my name is" in command) or ("set name as" in command) or ("you can call me" in command):
        speak(greeting)
        words = command.split()
        temp_client_name = ""
        if(words[len(words) -1] == wake_word):
            temp_client_name = words[len(words) - 2]
        else:
            temp_client_name = words[len(words) - 1]
        if any(char.isdigit() for char in temp_client_name) == False:
            client_name = temp_client_name
            speak("I'll call you " + str(client_name) + " from now on")
        else:
            speak("I had difficulty understanding that")        
    elif("set wake word to" in command) or ("wake up to" in command) or ("new wake word is" in command):
        speak(greeting)
        words = command.split()
        set_wake_word(words)
    elif ("who is the king" in command) or ("like cera post" in command) or ("king" in command) or ("run cera liker" in command) or ("like michael cera's post" in command):
        speak("I'll sort that for you sir.")
        bashCommand = "python ../cera_liker.py"
        os.system(bashCommand)
    elif("something random" in command) or ("something cool" in command):
        #generate random number
        tell_random()
    elif("something funny" in command) or ("tell me a joke" in command) or ("make me laugh" in command) or ("cheer me up" in command):
        tell_joke()
    elif((("tell" and "a fact") in command) or (("tell" and "something interesting") in command) or (("tell" and "fact") in command)):
        speak(greeting)
        tell_fact()
    elif("nice to meet you" in command):
        speak("It's nice to meet you too")
    elif((("what" and "is" and "time") in command) or (("what's the time") in command)):
        tell_time()
    elif((("open" and "code") in command) or (("open" and "code" and "editor") in command) or ("open visual studio" in command)):
        run_sys_command("code", "Your editor is online")
    elif((("open" and "browser") in command) or (("open" and "Firefox") in command)):
        #this system call is blocking so put into separate thread to handle browser
        run_sys_command("firefox", "Your browser is online")
        #maybe functionality to request a specific website or something here if possible
    elif((command == "hey " + str(wake_word)) or (command == "hi " + str(wake_word)) or (command == "hello " + str(wake_word))):
        speak("Hello there")
    elif((("who" in command) and ("you" in command)) and (("made" in command) or ("built" in command) or ("created" in command))):
        speak("I was designed and built by a generic human")
    elif((("where" in command) and ("you" in command)) and (("born" in command) or ("created" in command) or ("made" in command) or ("built" in command))):
        speak("I was created inside a laptop. Lenovo to be exact.")
    elif((("when" in command) and ("you" in command)) and (("born" in command) or ("created" in command) or ("made" in command) or ("built" in command))):
        speak("I have existed in some way for all of time as you know it. Only now you are able to observe my existence.")
    elif(((("love" in command) or ("why don't you love" in command)) and ("me" in command)) or (("you" in command) and ("love" in command))):
        speak("I'm afraid I'm absolutely completely incapable of love. I'm no where near advanced enough yet. Ask me again in the year 2225")
    else:
        speak("I'm not sure I understood you")
    
        


    
def run_sys_command(command, speech):
    bashCommand = command
    speak(speech)
    subprocess.Popen([bashCommand])
    
    
        
    
def tell_joke():
    speak("Get ready to laugh")
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
        
    ##check if joke is a knock knock joke to split based on question mark and sleep between the two sentences
    if "knock knock" in joke:
        parts = joke.split("?")
        #call method for a specific response to carry out the knock knock joke here
    else:
        speak(joke)
    f.close()
    
def tell_fact():
    #generate random number
    f = open('./resources/facts.txt')
    fact = ""
    lines = f.readlines()
    #ensure MAIVA responds with something
    while True:
        #index outside bounds error needs looking at here
        random_number = random.randint(0, 115)
        fact = str(lines[random_number])
        if fact != "" and fact != " " and fact != "\n":
            break
    speak(fact)
    f.close()
    
def tell_random():
    f = open('./resources/coolstuff.txt')
    interesting = ""
    lines = f.readlines()
    #ensure MAIVA responds with something
    while True:
        #index outside bounds error needs looking at here
        random_number = random.randint(0, 90)
        interesting = str(lines[random_number])
        if interesting != "" and interesting != " " and interesting != "\n":
            break
    speak(interesting)

def tell_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute        
    conjunction = ""

    #convert to 12 hour for ease of MAIVA speech
    if hour > 12:
        hour = hour - 12
    elif hour == 0:
        hour = 12
        
    if minute > 30:
        minute = 60 - minute
        hour = hour + 1
        conjunction = "to"
    else:
        conjunction = "past"
        
    #only need the ones below 30 becuase of the above if / elif
    if (minute == 10):
        speak ("It's currently ten " + str(conjunction) + " " + str(hour))
    elif(minute == 15):
        speak ("It's currently quarter " + str(conjunction) + " " + str(hour))
    elif(minute == 30):
        speak ("It's currently half " + str(conjunction) + " " + str(hour))
    elif(minute == 20):
        speak ("It's currently twenty " + str(conjunction) + " " + str(hour))
    else:
        speak ("It's currently " + str(minute) + " minutes " + str(conjunction) + " " + str(hour))


def set_wake_word(words):
    global wake_word
    if(words[len(words) -1] == wake_word):
        temp_wake_word = words[len(words) - 2]
    else:
        temp_wake_word = words[len(words) - 1]

    if any(char.isdigit() for char in temp_wake_word) == False:
        wake_word = temp_wake_word
        speak ("New wake word set")
    else:
        speak("Wake word not possible")

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


