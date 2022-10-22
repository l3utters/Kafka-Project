from kafka import KafkaConsumer
import json
from datetime import datetime
import time
import requests
import sys
from pymongo import MongoClient

# def internet_on():
    
#     url = "http://www.google.com"
#     timeout = 5    
#     try:
#         request = requests.get(url, timeout=timeout)
#         print("Connected to the Internet")
#         return True
#     except (requests.ConnectionError, requests.Timeout) as exception:
#         print("No internet connection.")
#         return False

# while internet_on():
    
try:

    consumer = KafkaConsumer('CandelaTemperature',bootstrap_servers='localhost:9092'
                              , client_id='PythonConsumer'
                              ,auto_offset_reset='earliest', enable_auto_commit=True
                              ,group_id='test-group6')
    
    print('Connected to Broker')
    
except:
    
    print('Could not Connect to Kafka Topic, please ensure Kafka Broker is running')
    enter = input('Press ENTER to close consumer')
    if enter == '':
    
        sys.exit('Closing Consumer Client')
        time.sleep(1)
        
try:
    
    client = MongoClient("mongodb://localhost:27017/")
    dbname = client['KafkaProject']
    collection_name = dbname["Light-Temp-Volt"]
    
except:
    
    print('Could not Connect to MongoDB, please ensure MongoDB is running')
    enter = input('Press ENTER to close producer')
    if enter == '':
    
        sys.exit('Closing Producer Client')
        time.sleep(1)
  
try:
    
    for message in consumer:
        
        timestamp = message.timestamp
        
        dt_object = datetime.fromtimestamp(timestamp/1000)
        
        value  = message.value.decode().strip()
        values = value.split(",")
        
        x = {
                "DateTime" :dt_object,
                "Temperature" : float(values[0]),
                "Lux" : float(values[1]),
                "Voltage" : float(values[2])
            }
        
        collection_name.insert_one(x)
        
        y = json.dumps(x, default = str)
        
        # r = requests.post("https://api.powerbi.com/beta/331c86e7-d032-436f-bc53-f2552d031012/datasets/0cf0e9ec-bb9d-4a74-9f61-5908ffee7d62/rows?key=isTD2vuKQoa8TFdxHG8GCmWWK79uSoCzgh9OnmI3EoHELdcyQOcE3aQBi1EJN6DWy0Za70T5GMlnvEvRkM1K0A%3D%3D",
                          # data="["+y+"]")
        
        # r = requests.post("https://api.powerbi.com/beta/331c86e7-d032-436f-bc53-f2552d031012/datasets/4c667fbc-bb25-44fc-98ce-021cd29b2961/rows?key=Cd%2F5hbsjavIcOToWGPYB%2B9VW3%2BPzttRkV7WbofE7O8QWY6D8K9COGmpW0j%2BZSSh%2Fb2YJnkoLRySPhWp2O%2FXCkA%3D%3D",
                          # data="["+y+"]")
        
        
        
        print(y)
        
except KeyboardInterrupt:
    consumer.close(autocommit=True)
    enter = input('Press ENTER to close producer')
    if enter == '':
    
        sys.exit('Closing Producer Client')
        time.sleep(1)

except:
    consumer.close(autocommit=True)
    enter = input('Press ENTER to close producer')
    if enter == '':
    
        sys.exit('Closing Producer Client')
        time.sleep(1)