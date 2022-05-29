import csv
from pathlib import Path
from datetime import datetime
import os
from record import getRecord


exportDir = os.path.join(Path(os.path.dirname(__file__)).parent.absolute(), 'Exports')
print(exportDir)

filename = 'May'+str(datetime.now().year)

header = ['Entry Number', 'Breakfast', 'Lunch', 'Dinner']
inFile = os.path.join(Path(exportDir).parent.absolute(), 'Records', filename+'.pickle')
exportFile = os.path.join(exportDir, filename+'.csv')

with open(exportFile, 'w', encoding='UTF8') as f:
    writer=csv.writer(f)
    writer.writerow(header)
    record = getRecord('May', '2022')
    for i in record:
        entry = []
        entry.append(i)
        for j in record[i]:
            entry.append(record[i][j])
        print(entry)
        writer.writerow(entry)