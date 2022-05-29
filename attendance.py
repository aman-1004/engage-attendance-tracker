from datetime import datetime
import numpy as np
import cv2 as cv
import face_recognition
import os
import time 
from helper.record import *

fileDirectory = Path(os.path.dirname(__file__)).absolute()


def postData(entryNumber:str, dtime: datetime, meal:str, toPost):
    toPost.append((entryNumber, dtime, meal))

def start(dtime: datetime, time_interval_seconds: int, meal:str, toPost):
    end_time = time.time() + time_interval_seconds
    path = os.path.join(fileDirectory, 'Images')
    images = []
    labels = []
    files = os.listdir(path)
    # print(path)
    # print(files)

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
                print("detected face:", name)
                postData(name, dtime, meal.lower(), toPost) 
                print("labels are:", labels)
                # To get coordinate of face in original image, coordinates of compressed Image are multiplied by 4 
                y1,x2,y2,x1 = list(map(lambda x: 4*x, faceLocation))
                cv.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 3)
                cv.rectangle(img, (x1,y2-35), (x2, y2), (0,255,0), cv.FILLED)
            if name:
                skip = True
                cv.putText(img,name, (x1+6, y2-6), cv.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                cv.imshow('WebCam', img)
                if cv.waitKey(1) & 0xFF == ord('q'): 
                    break
                # time.sleep(1) # Freeze for 1 second to allow attendee to confirm his attendance.

        if(not skip):
            cv.imshow('WebCam', img)
            if cv.waitKey(1) & 0xFF == ord('q'): 
                break
    if len(encodeListKnown):
        print("Time is over")

    cv.destroyAllWindows()
    cap.release()
meals = ['breakfast', 'lunch', 'dinner']


if __name__ == "__main__":
    toPost = []
    start(datetime.now(), 30, 'dinner', toPost)
    print(toPost)
    getRecord('Mar', 2022)