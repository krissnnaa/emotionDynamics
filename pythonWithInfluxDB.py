import influxdb
import re
from datetime import datetime

def readingData():
    DATA_PATH = '/home/krishna/Desktop/emotionDynamics/Carreau/'

    with open(DATA_PATH + 'Carreau_data.txt', 'r') as fd:
        dataFile = [l.strip().split('\t\t\t') for l in fd.readlines()][1:]

    with open(DATA_PATH + 'carreau_anger_intensities.txt', 'r') as fd:
        angerFile = [re.sub(r'\n', '', l) for l in fd.readlines()]

    with open(DATA_PATH + 'carreau_joy_intensities.txt', 'r') as fd:
        joyFile = [re.sub(r'\n', '', l) for l in fd.readlines()]

    with open(DATA_PATH + 'carreau_fear_intensities.txt', 'r') as fd:
        fearFile = [re.sub(r'\n', '', l) for l in fd.readlines()]

    with open('/home/krishna/Desktop/emotionDynamics/Carreau/carreau_sadness_intensities.txt', 'r') as fd:
        sadnessFile = [re.sub(r'\n', '', l) for l in fd.readlines()]

    carraeuFinalJson = []

    for item, anger, joy, fear, sad in zip(dataFile, angerFile, joyFile, fearFile, sadnessFile):
        createDate = re.findall(r'\d{4}-\d{2}-\d{2}', item[0])
        createDate = ''.join(createDate)
        dateForm = datetime.strptime(createDate, '%Y-%m-%d')
        ang = float(anger)
        joy = float(joy)
        fear = float(fear)
        sad = float(sad)
        msgDict = {}
        angDict = {}
        joyDict = {}
        fearDict = {}
        sadDict = {}
        fieldDict = {}
        user={}
        dataDict = {}
        msgDict['comments'] = item[1]
        angDict['anger'] = ang
        joyDict['joy'] = joy
        fearDict['fear'] = fear
        sadDict['sad'] = sad
        fieldDict.update(msgDict)
        fieldDict.update(angDict)
        fieldDict.update(joyDict)
        fieldDict.update(fearDict)
        fieldDict.update(sadDict)
        user['user']='carreau'
        dataDict['tags']=user
        dataDict['fields'] = fieldDict
        dataDict['time'] = (dateForm)
        dataDict['measurement'] = 'carreau_table'

        carraeuFinalJson.append(dataDict)
    return carraeuFinalJson

def insertIntoInfluxDB(carreuJson):

    client=influxdb.InfluxDBClient(host='localhost',port=8086)
    client.create_database('emotionDynamics')
    print(client.get_list_database())
    client.switch_database('emotionDynamics')

    print(client.write_points(carreuJson))

    results= client.query('SELECT "anger" FROM "emotionDynamics"."autogen"."carreau_table" GROUP BY "user"')
    #print(results.raw)
    points=results.get_points(tags={'user':'carreau'})
    for point in points:
        print('Time:%s, anger:%f' % (point['time'], point['anger']))

if __name__=='__main__':
    jsonFile=readingData()
    insertIntoInfluxDB(jsonFile)
