from datetime import datetime
from re import I
from turtle import update
import cv2 as cv
import numpy as np
import face_recognition
import os
import time 
import pickle

toPost = []
months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
fileDirectory = os.path.dirname(__file__)

def postData(entryNumber:str, dtime: datetime, meal:str):
    print((entryNumber, dtime, meal))
    toPost.append((entryNumber, dtime, meal))

def getRecord(month: str, year:str):
    pastRecord = None
    month_pickle =  os.path.join(fileDirectory, 'Records', month + str(year) + '.pickle')
    if (os.path.exists(month_pickle)):
        with open(month_pickle, 'rb') as file:
            pastRecord = pickle.load(file) 
        return pastRecord 
    else:
        return None

def updateRecord(dtime: datetime, toPost: list):
    updatedRecord = None
    month = months[dtime.month-1]
    month_pickle =  os.path.join(fileDirectory, 'Records', month + str(dtime.year) + '.pickle')
    print(month_pickle)
    if(os.path.exists(month_pickle)):
        updatedRecord = getRecord(month, dtime.year)
        for entryNumber,_, meal in toPost:
            if updatedRecord.get(entryNumber):
                updatedRecord[entryNumber][meal]+=1
            else:
                updatedRecord[entryNumber] = {
                    'breakfast': 0,
                    'lunch': 0,
                    'dinner': 0 
                    } 
                updatedRecord[entryNumber][meal]+=1
        with open(month_pickle,'wb+') as file:
            pickle.dump(updatedRecord, file)
    else:
        newRecord = {}
        for entryNumber,_,meal in toPost:
            newRecord[entryNumber]={
                    'breakfast': 0,
                    'lunch': 0,
                    'dinner': 0 
                    } 
            newRecord[entryNumber][meal]+=1
        with open(month_pickle,'wb+') as file:
            pickle.dump(newRecord, file)

def printRecord(month, year):
    record = getRecord(month, year)
    if record:
        for i in record:
            print(i, record[i])
    else:
        print("Record not available for this month")


def start(dtime: datetime, time_interval_seconds: int, meal:str):
    end_time = time.time() + time_interval_seconds
    path = os.path.join(fileDirectory, 'Images')
    print(path)
    images = []
    labels = []
    files = os.listdir(path)
    print(path)
    print(files)

    # Obtain list of names withuut extension. 
    for file in files:
        currentImg = cv.imread(f'{path}/{file}')
        images.append(currentImg)
        labels.append(os.path.splitext(file)[0])

    # Make face encodings of registered users.
    print(labels)
    encodeListKnown = []
    for img in images:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeListKnown.append(encode)

    cap = cv.VideoCapture(0)

    while len(labels) and time.time() < end_time:
        skip = False 
        status, img = cap.read()
        # Compressing Image to save computation time.
        imgCompressed = cv.resize(img, (0,0), None, 0.25, 0.25)
        imgCompressed = cv.cvtColor(imgCompressed, cv.COLOR_BGR2RGB)
        

        facesCurrentFrame = face_recognition.face_locations(imgCompressed)
        encodesCurrentFrame = face_recognition.face_encodings(imgCompressed, facesCurrentFrame)
        for encodeFace, faceLocation in zip(encodesCurrentFrame, facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            name = None
            if matches[matchIndex]:
                name = labels.pop(matchIndex)
                encodeListKnown.pop(matchIndex)
                postData(name, dtime, meal.lower()) 
                print(labels)
                # To get coordinate of face in original image, coordinates of compressed Image are multiplied by 4 
                y1,x2,y2,x1 = list(map(lambda x: 4*x, faceLocation))
                cv.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 3)
                cv.rectangle(img, (x1,y2-35), (x2, y2), (0,255,0), cv.FILLED)
            if name:
                skip = True
                cv.putText(img,name, (x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                cv.imshow('WebCam', img)
                if cv.waitKey(1) & 0xFF == ord('q'): break
                time.sleep(1) # Freeze for 1 second to allow attendee to confirm his attendance.

        if(not skip):
            cv.imshow('WebCam', img)
            if cv.waitKey(1) & 0xFF == ord('q'): break

    if len(encodeListKnown):
        print("Time is over")

meals = ['breakfast', 'lunch', 'dinner']

start(datetime.now(), 20, meals[2])
print('final post is' , toPost)

updateRecord(datetime.now(), toPost)
printRecord(months[datetime.now().month-1], datetime.now().year)