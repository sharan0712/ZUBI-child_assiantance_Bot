import sys
import pandas as pd
import numbers
import xlrd
from gtts import gTTS
from googletrans import Translator
import vlc
from twilio.rest import Client
import io,cv2
from google.cloud import vision
import os
import time
import pyaudio
import speech_recognition as sr
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
df=pd.read_excel('/home/pi/christ1_FAQ.xlsx',sheet_name=0)#default FAQs are written to enchance the bot interactions.

questions= list(df['Questions'])

answers=  list(df['Answers'])
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'api key.json'
SOURCE_PATH = '/home/pi/Zubi'
r = sr.Recognizer()
languages={'arabic':'ar','bengali':'bn','english':'en','gujarati':'gu','hindi':'hi','kannada':'kn','malayalam':'ml','marathi':'mr','tamil':'ta','telugu':'te','urdu':'ur'}
def helpme():
    account_sid =""#Use your Account iD
    auth_token =""#use your token ID
    client = Client(account_sid, auth_token)
    message = client.api.account.messages.create(to="+918",from_="+1 41",body='i am in danger please help me')#dummy phone numbers are created
    response='help will arrive soon'
    return response
   
def translator():
    a=0
    while a==0:
        print('Choose language you want to translate from')
        audio1=input()
        print ('Choose language you want to translate to')
        audio3 =input()
        if audio1 in languages.keys() and audio3 in languages.keys():
            id=languages[audio1]
            id1=languages[audio3]
            print("type the sentence to translate")
            trans=input()
            translator = Translator()
            output=translator.translate(trans,dest=id1)
            #print (output.text)
            spo1=gTTS(text=output.text,lang=id1,slow=False)
            spo1.save("b.mp3")
            b=vlc.MediaPlayer('/home/pi/b.mp3')
            b.play()
            time.sleep(4)
            a=1

        elif audio1 in languages.keys() and audio3 not in languages.keys():
            print ("The language you want to translate from is not in the list, choose again")
            continue
        elif audio1 not in languages.keys() and audio3 in languages.keys():
            print ("The language you want to translate to is not in the list, choose again")
            continue
    response=output.text
    return response
   
def recognize_item():
    b=0
    while b==0:
        print('Say ready when you are focusing the camera on the object to recognize ')
        image1=input()
        if image1=='ready':
            print('Capturing of the Image ')
            c=cv2.VideoCapture(0)
            ret , image = c.read()
            if ret:
                cv2.imwrite('/home/pi/SampleImage.jpg',image)
            c.release()
            print('Image is Captured')
            print(' Now Recognizing the Captured the Image ')
            img_path = SOURCE_PATH + '/{}'.format('SampleImage.jpg')
            b=1
        else:
            continue
       
    client = vision.ImageAnnotatorClient()
    with io.open(img_path, 'rb') as image_file:
        content = image_file.read()
        image = vision.types.Image(content=content)
        response1 = client.label_detection(image=image)
        labels = response1.label_annotations
        for label in labels:
            desc = label.description.lower()
            print("The Name of the Image is " +desc.upper())
            g=gTTS(text=desc.upper(),lang='en',slow=True)
            g.save('i.mp3')
            i=vlc.MediaPlayer('/home/pi/Zubi/i.mp3')
            i.play()
            time.sleep(5)
            break
    response=desc.upper()
    return response
def list_faq():
    print("These are some of the questions u can ask")
    for i in range(len(questions)):
        print(str(i)+":"+questions[i])
       
def check_for_faq_index():
    list_faq()
    question_id=input(" do you have a question for me?")
    response=""
             
   
    if "no" in question_id:
        print("Thank YOU!")
        GPIO.output(18,GPIO.LOW)
        exit()
    while True:
                if "no" in question_id:
                    print("Thank YOU! Have a good day")
                    GPIO.output(18,GPIO.LOW)
                    exit()
                if "bye" in question_id:
                    print("Thank YOU! Have a good day")
                    GPIO.output(18,GPIO.LOW)
                    exit()
                elif question_id in questions:
                    index=questions.index(question_id)
                    response=answers[index]
                elif question_id=="translate":
                    response=translator()
                elif question_id=="capture":
                    response=recognize_item('/home/pi/cool.jpg')
                elif question_id=="help":
                    response=helpme()
                else:
                    response="Sorry! I do not know the answer to that question!"
                    print("Do you have any other question for me?")
                return response
                   
print("..................")
print("Enter B-code to start zubi")
b=input()
if b=="start":
    print("uploading all data to zubi")
    GPIO.output(18,GPIO.HIGH)
   
    print("Hello! Im zubi here to serve you")
    while True:
        response=check_for_faq_index()
        print("Your BOT: "+response)
