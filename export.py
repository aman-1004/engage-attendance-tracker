import csv
from pathlib import Path
from datetime import datetime
import os
from helper.record import getRecord 

exportDir = os.path.join(Path(os.path.dirname(__file__)), 'Exports')
filename = 'May'+str(datetime.now().year)


def recordsAvailable():
    recordDir = os.path.join(Path(exportDir).parent, 'Records')
    return list(map(lambda x: os.path.splitext(x)[0], os.listdir(recordDir)))

def export(filename:str , exportDir: os.path):
    header = ['Entry Number', 'Breakfast', 'Lunch', 'Dinner']
    inFile = os.path.join(Path(exportDir).parent.absolute(), 'Records', filename+'.pickle')
    exportFile = os.path.join(exportDir, filename+'.csv')
    print("Exporting records to:", exportFile)
    with open(exportFile, 'w', encoding='UTF8') as f:
        writer=csv.writer(f)
        writer.writerow(header)
        record = getRecord(filename[0:3], filename[3:])
        for i in record:
            entry = []
            entry.append(i)
            for j in record[i]:
                entry.append(record[i][j])
            writer.writerow(entry)


if __name__ == "__main__":
    print('Inside main of export.py')
    export(recordsAvailable()[0], exportDir)