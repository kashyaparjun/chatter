import json

def readFile():
    myFile=open("./data/trailer.json", 'r')
    myObject=myFile.read()
    u = myObject.decode('utf-8-sig')
    myObject = u.encode('utf-8')
    myFile.encoding
    myFile.close()
    myData=json.loads(myObject,'utf-8')
    return myData

def writeFile(j):
    with open('./data/trailer.json', 'w+') as outfile:
        json.dump(j, outfile)