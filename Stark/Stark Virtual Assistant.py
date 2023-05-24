import pyttsx3 
from datetime import datetime
import speech_recognition as sr
import wikipedia as wiki
import webbrowser as wb
import os,sys
from googlesearch import * 
import getpass4
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys  
import re 
import mysql.connector
import smtplib
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

engine = pyttsx3.init()
r = sr.Recognizer()

def speak(audio):
    voice_id="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
    engine.setProperty('voice', voice_id)
    engine.say(audio)
    engine.runAndWait()

def time():
    now = datetime.now()
    Time = now.strftime("%H:%M:%S")
    print(Time)
    speak(Time)

def date():
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    Date = now.strftime("%m/%d/%Y")
    print(Date)
    speak(Date)
    
def wishme():
#     speak("Welcome Back Sir!")
#     speak("Current time is ")
#     time()
#     speak("Current date is ")
#     date()
    now = datetime.now()
    hour=now.hour
    if hour>=6 and hour<12 :
        speak("Good Morning Sir!") 
    elif hour>=12 and hour<18:
        speak("Good Afternoon Sir !")
    else:
        speak("Good Evening Sir !")
    speak("STARK at your service. Please tell me how can I help You?")
    

stemmer = WordNetLemmatizer()


def preprocess_text(document):
    
    document = re.sub(r'\W',' ', str(document)) ## Removing Special Characters ##
    
    document = re.sub(r'\s+[a-zA-Z]\s+',' ', document) ## Removing all single Characters ##
    
    document = re.sub(r'\^[a-zA-Z]\s+',' ', document) ## Removing single Characters from start ##
    
    document = re.sub(r'\s+',' ',document, flags=re.I) ## Removing Special CharactersSubstituting multiple space with single space ##
     
    document = re.sub(r'^b\s',' ', document) ## Removing prefixed 'b' ##
    
    document = document.lower() ## Converting to lower cases ##
    
    tokens = document.split()
    tokens = [stemmer.lemmatize(word) for word in tokens]
    tokens = [word for word in tokens if word not in en_stop]
    tokens = [word for word in tokens if len(word) > 5]
    db = mysql.connector.connect(username='root', passwd='',
                             host='localhost', database = 'test')
    dbcur = db.cursor()
    #sqlcommand = (" insert into yourtext values ('"+tokens+"')")#
    query = "select * from {}".format(tokens[0])
    dbcur.execute(query)
    print(dbcur.fetchall())
    #dbcur.execute(sqlcommand)#
    dbcur.execute("commit")
    dbcur.close()
    #print(tokens,file = open("yourtext.txt","a"))
    
    return tokens

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio=r.adjust_for_ambient_noise(source, duration=0.1)
        print("Listening..")
#         r.pause_threshold = 0.1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(query)
    
    except Exception as e:  
        print(e)
        speak("Say that again please")
        return "None"
    return query

def askpermission():
    print("Do you want me to do anything else....?")
    speak("Do you want me to do anything else....?")

    d = takecommand().lower()
    if (d=='no'):
        print("Okay!!! Stark Going offline...Thankyou !")
        speak("Okay!!! Stark Going offline...Thankyou !")
    elif (d=='yes'):
        print("What task you wish to do ?....! I am Listening...")
        speak("What task you wish to do ?....! I am Listening...")
        perform_tasks()
        askpermission()
    else:
        speak("I did not get that....Can you repeat")
        askpermission()
        
            
def perform_tasks():
    query = takecommand().lower()
    if 'time' in query :
        time()

    elif 'date' in query:
        date()

    elif 'how are you' in query:
        speak("I am fine ! Thankyou. How may I help you?")
    elif 'thank you' in query:
        print("Happy to help you..!")
        speak("Happy to help you..!")

    elif 'play song'in query:
        songs_dir= 'D:\\Songs'
        songs= os.listdir(songs_dir)
        os.startfile(os.path.join(songs_dir , songs[0]))
    
    elif 'today' in query:
        query = takecommand().lower()
        print(query)
        tokens = preprocess_text(query)
        print(tokens)
        

    elif 'send email' in query:
        try: 
            speak("What is your message?")
            content= takecommand()
            print(content)
            to = take_email_address()
            print("Are you sure you want to send following mail to "+to+" with following content:-\n"+content)
            speak("Are you sure you want to send following mail to "+to+" with following content:-\n"+content)
            confirm = takecommand().lower()
            if 'yes' in confirm:
                sendemail(to, content)
                speak("Email sent Successfully..!")
            else:
                print("Email sending failed...!!!")
                speak("Email sending failed...!!!")

        except Exception as e:
            print(e)
            print("Unable to send email due to technical reasons. Please try again later!")
            speak("Unable to send email due to technical reasons. Please try again later!")

    
    elif 'whatsapp' in query:
        my_contacts={
                     "urvi": {"name":"urvi","phone":"917433834882"}
                    }
        speak("I am Opening Whatsapp. Please Keep your phone in your hand to scan QR code.")
        speak("Kindly note that you will get maximum 10 seconds")
        driver = whatsapp_login()
        speak("Whatsapp opened Successfully")
        speak("Would You like to Message someone...??")
        ch=takecommand()
        if(ch=='yes'):
            speak("Whom do You Want to send message..? ")
            speak("Please enter name as saved in your contacts")
            name= takecommand().lower()
            print(name)
            if name in my_contacts:
                speak("Contact found")
                number=my_contacts[name]["phone"]

            else:
                speak("Contact Doesn't exist. If You have number than please enter below as shown in format")
                number=input("Enter number(eg: 911234567890 not +91 1234567890)")

            speak("Please speak your Message")
            msg=takecommand()

            print("Following Message will be sent to "+number+"\n"+msg)
            print("Sure to continue")
            speak("Sure to continue")
            choice=takecommand().lower()
            if choice=="yes":
                whatsapp_sender(msg,number,driver)
                speak("MESSAGE SENT SUCCESSFULLY")
            else:
                print("MESSAGE SENDING FAILED..!!")
                speak("MESSAGE SENDING FAILED..!!")
        else:
            driver.maximize_window()

    else:
        print("Kindly Repeat Yourself...")
        speak("Kindly Repeat Yourself...")
        perform_tasks()
        
        
def whatsapp_login():
    import time
    driver = webdriver.Firefox(executable_path=r"D:\geckodriver-v0.27.0-win64\geckodriver.exe")
    driver.get("https://web.whatsapp.com/")
    time.sleep(10)
    return driver

def whatsapp_sender(msg,number,driver):
    import time
    driver.maximize_window()
    link = "https://web.whatsapp.com/send?phone={}&text&source&data&app_absent".format(number)
    driver.get(link)
    time.sleep(7)
    input_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    for ch in msg:
        if ch == "\n":
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.BACKSPACE).perform()
        else:
            input_box.send_keys(ch)
    input_box.send_keys(Keys.ENTER)
    time.sleep(5)
    driver.close()
def sendemail(to, content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    print("Please enter your Password")
    speak("Please enter your Password")
    pwd = getpass4.getpass('Password :: ')
    if(pwd=="Urvi260199"):
        server.login("patelurvi19172@gmail.com",pwd)
        server.sendmail("patelurvi19172@gmail.com", to, content)
        server.close()
    else:
        speak("Password NOt Correct...!!! Please try again later")
        
def take_email_address(): 
    print("WHom do you wish to send this mail?")
    speak("WHom do you wish to send this mail?")
    email_add = input("Enter email address: ")
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    while((re.search(regex,email_add)) == False):
        print("Entered email is in-valid....Kindly try again..")
        speak("Entered email is in-valid....Kindly try again..")
        email_add = input("Enter email address: ") 
    return email_add

wishme()
perform_tasks()
askpermission()