from kafka import KafkaConsumer
import json
from datetime import datetime
import time
import requests
import sys
from pymongo import MongoClient
    
try:

    topic_name = 'CandelaTemperature'
    client_name = 'PythonConsumer'
    group_name = 'test-group'

    consumer = KafkaConsumer(topic_name,
                             bootstrap_servers='localhost:9092',
                             client_id=client_name,
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id=group_name)
    
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