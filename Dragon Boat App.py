
# coding: utf-8

# In[1]:


from flask import Flask, request
from flask_cors import CORS
import json
import os
app = Flask(__name__)
CORS(app)

mockdb = {"heats":[], "stateId":0}

boatCounter = 0
heatCounter = 0

@app.route("/")
def index():
    root_dir = os.path.dirname(os.getcwd())
    return app.send_static_file('index.html')

@app.route('/addHeat',methods=['POST'])
def addHeat():
    global heatCounter
        
    mockdb["heats"].append({"id":str(heatCounter),"boats":[]})
    heatCounter+=1
    mockdb["stateId"] += 1
    return json.dumps(mockdb)

@app.route('/<heatId>/addBoat',methods=['POST'])
def addBoat(heatId):
    global boatCounter
    heat = [heat for heat in mockdb["heats"] if heat["id"] == heatId]
    if not heat:
        return '{"error": "Heat not found"}'
    Id = str(boatCounter)
    heat[0]["boats"].append({"id":Id,"name":"Boat " + Id,"color":None,"StartTime":None,"EndTime":None})
    boatCounter+=1
    mockdb["stateId"]+=1
    return json.dumps(mockdb)

@app.route('/<heatId>/deleteHeat',methods=['POST'])
def deleteHeat(heatId):
    mockdb["heats"] = [heat for heat in mockdb["heats"] if heat["id"] != heatId]
    mockdb["stateId"] += 1
    return json.dumps(mockdb)

@app.route('/<heatId>/<boatId>/deleteBoat',methods=['POST'])
def deleteBoat(heatId,boatId):
    heat = [heat for heat in mockdb["heats"] if heat["id"] == heatId]
    if not heat:
        return '{"error": "Heat not found"}'
    heat[0]["boats"] = [b for b in heat[0]["boats"] if b["id"] != boatId]
    
    mockdb["stateId"] += 1
    return json.dumps(mockdb)

def setBoatParm(heatId,boatId,k,v):
    heat = [heat for heat in mockdb["heats"] if heat["id"] == heatId]
    if not heat:
        return '{"error": "Heat not found"}'
    boat = [boat for boat in heat[0]["boats"] if boat["id"] == boatId]
    if not boat:
        return '{"error": "Boat not found"}'
    boat[0][k] = v
    
    mockdb["stateId"] += 1
    
    return json.dumps(mockdb)

@app.route('/<heatId>/setHeatStartTime',methods=['POST'])
def setHeatStartTime(heatId):
    heat = [heat for heat in mockdb["heats"] if heat["id"] == heatId]
    if not heat:
        return '{"error": "Heat not found"}'
    reqJSON = request.get_json()
    for boatId in (boat["id"] for boat in heat[0]["boats"]):
        setBoatParm(heatId, boatId, "StartTime", reqJSON["StartTime"])
    return json.dumps(mockdb)


@app.route('/<heatId>/<boatId>/setStartTime',methods=['POST'])
def setStartTime(heatId,boatId):
    reqJSON = request.get_json()
    if not "StartTime" in reqJSON:
        return '{"error": "missing start time"}'
    return setBoatParm(heatId,boatId,"StartTime",reqJSON["StartTime"])

@app.route('/<heatId>/<boatId>/setEndTime',methods=['POST'])
def setEndTime(heatId,boatId):
    reqJSON = request.get_json()
    if not "EndTime" in reqJSON:
        return '{"error": "missing end time"}'
    return setBoatParm(heatId,boatId,"EndTime",reqJSON["EndTime"])

@app.route('/<heatId>/<boatId>/setName',methods=['POST'])
def setName(heatId,boatId):
    reqJSON = request.get_json()
    if not "Name" in reqJSON:
        return '{"error": "missing name"}'
    return setBoatParm(heatId,boatId,"name",reqJSON["Name"])

@app.route('/<heatId>/<boatId>/setColor',methods=['POST'])
def setColor(heatId,boatId):
    reqJSON = request.get_json()
    if not "Color" in reqJSON:
        return '{"error": "missing color"}'
    return setBoatParm(heatId,boatId,"color",reqJSON["Color"])

@app.route('/resetState',methods=['POST'])
def resetState():
    global mockdb
    global boatCounter
    global heatCounter
    mockdb = {"heats":[], "stateId":mockdb["stateId"]}
    boatCounter = 0
    heatCounter = 0
    return mockdb

@app.route('/getState',methods=['POST'])
def getState():
    reqJSON = request.get_json()
    print(reqJSON)
    if reqJSON and ("stateId" in reqJSON) and (mockdb["stateId"] == reqJSON["stateId"]):
        return '{"unchanged": 1}'
    return json.dumps(mockdb)


# In[ ]:


if __name__ == "__main__":
    app.run()

