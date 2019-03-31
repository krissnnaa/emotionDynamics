import csv
import re
from datetime import datetime

DATA_PATH='/home/krishna/Desktop/emotionDynamics/Carreau/'

with open(DATA_PATH+'Carreau_data.txt','r') as fd:
    dataFile= [l.strip().split('\t\t\t') for l in fd.readlines()][1:]

with open(DATA_PATH+'carreau_anger_intensities.txt','r') as fd:
    angerFile=[re.sub(r'\n','',l) for l in fd.readlines()]

with open(DATA_PATH+'carreau_joy_intensities.txt','r') as fd:
    joyFile=[re.sub(r'\n','',l) for l in fd.readlines()]

with open(DATA_PATH+'carreau_fear_intensities.txt','r') as fd:
    fearFile=[re.sub(r'\n','',l) for l in fd.readlines()]

with open('/home/krishna/Desktop/emotionDynamics/Carreau/carreau_sadness_intensities.txt','r') as fd:
    sadnessFile=[re.sub(r'\n','',l) for l in fd.readlines()]


with open(DATA_PATH+'Carreu_file.csv','w') as csvfile:
    csvObject=csv.writer(csvfile,delimiter=',', quoting=csv.QUOTE_MINIMAL)
    for item,anger,joy,fear,sad in zip(dataFile,angerFile,joyFile,fearFile,sadnessFile):
        createDate=re.findall(r'\d{4}-\d{2}-\d{2}',item[0])
        createDate=''.join(createDate)
        dateForm=datetime.strptime(createDate,'%Y-%m-%d')
        csvObject.writerow([dateForm,item[1],float(anger),float(joy),float(fear),float(sad)])
