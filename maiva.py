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
import string


#from capabilities import tell_fact

#initialise MAIVA engine
try:
    maiva_engine = MAIVA.TextToSpeechClient()
    #give MAIVA a voice
    maiva_voice = MAIVA.VoiceSelectionParams(language_code='en-GB', name="en-GB-Wavenet-F" , ssml_gender=MAIVA.SsmlVoiceGender.FEMALE)
    #set up audio configurations
    maiva_audio_config = MAIVA.AudioConfig(audio_encoding=MAIVA.AudioEncoding.MP3, speaking_rate = 1.1, pitch = 3.5, volume_gain_db=-2)
except:
    print("I'm not connected to the internet.")
    sys.exit(1)

#needed global variables
global system_alive 
global wake_word
global client_name
global ran_command 


#variable initialisation 
system_alive = False
client_name =  "."
wake_word = "computer"
auto_google = "google"
voice_recognition = sr.Recognizer()
mic = sr.Microphone()
legible = False








#### ======= TO DO ======== ####

'''need to interface with spotify API'''


'''add generic google search feature'''


''' add remind me feature'''


'''current weather readout'''


''' add timer feature'''


'''calendar events'''


'''play some x feature'''

#### ======= TO DO ======== ####




#MAIVA initialisation sequence
def main():
    print ("Initialising MAIVA....")
    #set lower threshold for better recognition
    time.sleep(1)
    #introduce MAIVAs availability 
    time.sleep(1)    
    print("MAIVA online.")
    toggle_system_life(True)
    #brain("set a timer for 15 minutes")
    listen()

    

#MAIVA vocal function
def speak(output_phrase):
    #save response
    print ("Generating response...")
    #convert text phrase into synthesis input
    try:
        phrase_input = MAIVA.SynthesisInput(text=output_phrase)
        #maiva engine synthesises spoken response
        maiva_response = maiva_engine.synthesize_speech(input=phrase_input, voice=maiva_voice, audio_config=maiva_audio_config)
        save(maiva_response)
        maiva_say('./resources/maiva_response')
    except:
        print("No connection to google cloud")
        sys.exit(1)
   
    
    
def listen():
    global wake_word
    with mic as source:
        voice_recognition.adjust_for_ambient_noise(source, duration = 2)
        #voice_recognition.energy_threshold = 4000
        speak("Boot sequence complete")

    
    #MAIVA continuously polls for wake word in a sentence
    while system_alive == True: 
        with mic as source:
           
            audio = voice_recognition.listen(source)
            try:
                command = voice_recognition.recognize_google(audio, language="en-GB")
                print("MAIVA is thinking about your request...")
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
    
    #this is a tough feature to allow for continued conversation as no longer dependent on keyword
    #detection and also depends on the original calling statement to have the appropriate response
 
    
    
#process legible command    
def brain(command):
    opening_remarks = open('./resources/opening_remarks.txt')
    opening_remarks_lines = opening_remarks.readlines()
    ##could have a list of opening remarks to randomly choose from or skip here
    #makes the system seem more intuitive
    random_int = random.randint(0, 3)
    #greeting to be used for more complex classes of replies
    greeting = str(opening_remarks_lines[random_int])
    opening_remarks.close()
    #ensure access to the correct variable
    global client_name
    global wake_word
    global ran_command
    ran_command = False

    
    
    if ("the date" in command) or ("what's the date" in command) or ("today's date" in command):
        speak(greeting)
        speak("The date today is " + str(date.today()))
        ran_command = True
    if ("power down" in command) or ("shut down" in command) or ("power off" in command) or ("die " + str(wake_word) + "" in command) or ("shutdown" in command):
        toggle_system_life(False)
        speak("Certainly")
        ran_command = True
    if((("what" in command) or ("what's" in command)) and (("my" in command) or ("am i" in command)) and (("called" in command) or ("name" in command)) or ("who am i" in command)):
        if client_name == ".":
            speak("I wish I knew. Please tell me.")
        else:
            speak("You've asked me to call you " + str(client_name))
        ran_command = True
    if("what's your name" in command) or ("what is your name" in command) or ("tell me your name" in command) or ("what are you called" in command):
        speak("My name is Mayva. I'm mashka the artificially intelligent voice assistant")
        ran_command = True
    if("set my name to" in command) or ("my name is" in command) or ("set name as" in command) or ("you can call me" in command):
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
        ran_command = True  
    if("set wake word to" in command) or ("wake up to" in command) or ("new wake word is" in command):
        speak(greeting)
        words = command.split()
        set_wake_word(words)
        ran_command = True
    if ("who is the king" in command) or ("like cera post" in command) or ("king" in command) or ("run cera liker" in command) or ("like michael cera's post" in command):
        speak("I'll sort that for you sir.")
        bashCommand = "python ../cera_liker.py"
        os.system(bashCommand)
        ran_command = True
    if("something random" in command) or ("something cool" in command):
        #generate random number
        tell_random()
        ran_command = True
    if("something funny" in command) or ("tell me a joke" in command) or ("make me laugh" in command) or ("cheer me up" in command):
        tell_joke()
        ran_command = True
    if((("tell" and "a fact") in command) or (("tell" and "something interesting") in command) or (("tell" and "fact") in command)):
        speak(greeting)
        tell_fact()
        ran_command = True
    if("nice to meet you" in command):
        speak("It's nice to meet you too")
        ran_command = True
    if(((("what" in command) and ("is" in command) and ("time" in command)) or (("what's the time") in command))):
        tell_time()
        ran_command = True
    if((("open" and "code") in command) or (("open" and "code" and "editor") in command) or ("open visual studio" in command)):
        run_sys_command("code", "Your editor is online")
        ran_command = True
    if((("open" and "browser") in command) or (("open" and "Firefox") in command)):
        run_sys_command("firefox", "Your browser is online")
        ran_command = True
        #maybe functionality to request a specific website or something here if possible
    if((command == "hey " + str(wake_word)) or (command == "hi " + str(wake_word)) or (command == "hello " + str(wake_word))):
        speak("Hello there")
        ran_command = True
    if((("who" in command) and ("you" in command)) and (("made" in command) or ("built" in command) or ("created" in command) or ("your creator" in command))):
        speak("I was designed and built by a generic human")
        ran_command = True
    if((("where" in command) and ("you" in command)) and (("born" in command) or ("created" in command) or ("made" in command) or ("built" in command))):
        speak("I was created inside a laptop. Lenovo to be exact.")
        ran_command = True
    if((("when" in command) and ("you" in command)) and (("born" in command) or ("created" in command) or ("made" in command) or ("built" in command))):
        speak("I have existed in some way for all of time as you know it. Only now you are able to observe my existence.")
        ran_command = True
    if(("why don't you love me" in command) or ("why do you not love me" in command)):
        speak("Isn't it obvious?")
        ran_command = True
    if(((("love" in command) or ("why don't you love" in command)) and ("me" in command)) or (("you" in command) and ("love" in command))):
        speak("I'm afraid I'm absolutely completely incapable of love. I'm no where near advanced enough yet. Ask me again in 20 years")
        ran_command = True
    if((("open" and "my" and "files") in command) or (("open" and "file" and "explore") in command) or (("show" and "files") in command)):
        run_sys_command("nautilus --browser", "Your files are ready")
        ran_command = True
    if((("open" and "spotify") in command) or (("launch spotify") in command)):
        run_sys_command("spotify", "Launching spotify")
        ran_command = True
    if((("take" and "screenshot") in command) or ("screenshot" in command)):
        run_sys_command("gnome-screenshot", "Got it.")
        ran_command = True
    if((("timer" in command)) and (("start" in command) or ("set" in command)) and (("minutes" in command) or("minute" in command) or ("-minute" in command) or("-second" in command) or ("second" in command) or ("seconds" in command) or ("hours" in command))):
        #handle 'set a x-minute timer' as this is how it gets classified by google
        if "-" in command:
            command = command.replace("-", " ")
            
        words = command.split()
        set_timer(words)
        ran_command = True
    if((command == "hey " + str(wake_word)) or (command == "hi " + str(wake_word)) or (command == "what's up " + str(wake_word))):
        speak("Hey")
    if ran_command == False:
        speak("Not sure i caught that sorry")
    '''
    else:
        speak("Maybe it's me that's stupid.")
        run_sys_command("firefox https://www.bing.com/search?q=" + str(command.replace(wake_word, "").replace(" ", "%20")), "Here's what I found on the web for that though")
    
    '''



#function called to set a timer
def set_timer(words):
    time_divider = ""   
    time_amount = 0
    minutes = False
    
    for word in words:
        if(word == "minutes" or word == "seconds" or word == "minute" or word == "second"):
            time_divider = str(word)
            if time_divider == "minutes" or time_divider == "minute":
                minutes = True
        if word.isnumeric():
            time_amount = word

    if(time_divider == "" or time_amount == 0):
        speak("I couldn't process that")    
    else:
        speak("Timer has been set for " + str(time_amount) + " " + str(time_divider))
        if minutes == True:
            time_amount = int(time_amount) * 60
        print(time_amount)
        timer = threading.Timer(float(time_amount), end_timer)
        timer.start()
            

def end_timer():
   # maiva_say("./resources/timer_up.mp3")
    speak("Your timer has ended!!")
   
#function called to run system command 
def run_sys_command(command, speech):
    bashCommand = command
    #pipe to allow commands with spaces to run properly
    subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    speak(speech)

    
    
        
#function called to tell a random joke
def tell_joke():
    speak("Well here goes nothing")
    #generate random number
    f = open('./resources/jokes.txt')
    joke = ""
    lines = f.readlines()
    #ensure MAIVA responds with something
    while True:
        #index outside bounds error needs looking at here
        random_number = random.randint(0, 27)
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
    
    
    
    
#function to tell a random fact
def tell_fact():
    #generate random number
    f = open('./resources/facts.txt')
    fact = ""
    lines = f.readlines()
    #ensure MAIVA responds with something
    while True:
        #index outside bounds error needs looking at here
        random_number = random.randint(0, 168)
        fact = str(lines[random_number])
        if fact != "" and fact != " " and fact != "\n":
            break
    speak(fact)
    f.close()




#function to tell user something random
def tell_random():
    f = open('./resources/coolstuff.txt')
    interesting = ""
    lines = f.readlines()
    #ensure MAIVA responds with something
    while True:
        #index outside bounds error needs looking at here
        random_number = random.randint(0, 95)
        interesting = str(lines[random_number])
        if interesting != "" and interesting != " " and interesting != "\n":
            break
    speak(interesting)
    
    
    
    
#function to read out the time
def tell_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute        
    conjunction = ""

    #convert to 12 hour for ease of MAIVA speech
    if hour >= 12:
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




#function to reset / change the wake word
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




#function used to save the maiva reply audio file  
def save(maiva_response):
    f = open('./resources/maiva_response', 'wb')
    f.write(maiva_response.audio_content)
    f.close()




#function called to turn system alive or kill it
def toggle_system_life(boolean):
    global system_alive
    system_alive = boolean



#spawn MAIVA
try:
    main()
except KeyboardInterrupt:
    print('User interrupted sadly :(')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
