from datetime import datetime
import os
import time
import pickle
from pathlib import Path
months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

recordDirectory = Path(os.path.dirname(__file__)).parent.absolute()
def getRecord(month: str, year:str):
    pastRecord = None
    month_pickle =  os.path.join(recordDirectory, 'Records', month + str(year) + '.pickle')
    if (os.path.exists(month_pickle)):
        with open(month_pickle, 'rb') as file:
            pastRecord = pickle.load(file) 
        return pastRecord 
    else:
        return None

def updateRecord(dtime: datetime, toPost: list):
    updatedRecord = None
    month = months[dtime.month-1]
    month_pickle =  os.path.join(recordDirectory, 'Records', month + str(dtime.year) + '.pickle')
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
