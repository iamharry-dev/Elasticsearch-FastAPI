from cgitb import text
from fastapi import FastAPI, Header
from pydantic import BaseModel
from elasticsearch import Elasticsearch
import uuid

app = FastAPI()

class Text(BaseModel):
    text: str

async def generateUUID():
	return uuid.uuid1()

#POST to create new data
@app.post("/create_fields")
async def createData(company_name: Text,floor: Text,group:Text , camera : Text , videos: Text):
    uid = await generateUUID()

    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    res = es.index(index="fraction", id=uid, body={"company_name": company_name.text , 
                      "floor": floor.text , "group" : group.text , "camera":camera.text , "videos": videos.text
                      })
    es.indices.refresh(index="fraction")
    return(uid)

#GET all data stored
@app.get("/get_all")
def getData():
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    es.indices.refresh(index="fraction")
    res = es.search(index="fraction", body={"query": {"match_all": {}}})
    return res

#GET specific data using 
@app.get("/specific_data")
def getDataFromId(company_name: str):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    es.indices.refresh(index="fraction")
    res = es.search(index="fraction", body={'query':{'match':{'company_name':company_name}}})
    return res
