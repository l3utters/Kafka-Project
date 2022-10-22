from pymongo import MongoClient
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from datetime import timedelta

now = datetime.now()

try:
    client = MongoClient("mongodb://localhost:27017/")
    dbname = client['Candela-Temperature']
    collection_name = dbname["KafkaTest"]
    
    minback10 = now - timedelta(minutes=1)
    
    query =  {'DateTime':{'$gte':minback10,'$lt':now}}
    
    items = collection_name.find(query)
    
    # items = list(collection_name.find())
    df_ts = pd.DataFrame(items)
    client.close()
except:
    client.close()