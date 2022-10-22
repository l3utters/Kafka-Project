import serial
from kafka import KafkaProducer
import time
import sys

#Tries to connect to the Kafka topic, if connection is successful code goes on
#otherwise an exception is thrown showing the connection failed and prompts to
#press enter to close the script
try:

    producer = KafkaProducer(bootstrap_servers='localhost:9092', client_id='PythonProducer'
                                ,acks='all', retries=0) 
    
    print('Connected to Broker')
    
except:
    
    print('Could not Connect to Kafka Topic, please ensure Kafka Broker is running')
    enter = input('Press ENTER to close producer')
    if enter == '':
    
        sys.exit('Closing Producer Client')
        time.sleep(1)

#Attempts to connect to the serial port COM4, commonly used by the arduino and
#further gathers the sensor readings from the serial port and commits them to
#the Kafka topic one-by-one
try:

    ser = serial.Serial('COM4', 9600)
    time.sleep(2)

    while(True):
        
        serialString = ser.readline()
        
        serialString = serialString.decode()
        
        serialString = serialString.strip()
        
        num_int = bytes(serialString, encoding='UTF-8')
    
        print(num_int)
        
        producer.send('CandelaTemperature', num_int, num_int)
        
except KeyboardInterrupt:
    ser.close()
    print('Serial Port Closed')
    producer.close()
    print('Producer Closed')
    enter = input('Press ENTER to close producer')
    if enter == '':
    
        sys.exit('Closing Producer Client')
        time.sleep(1)

except:
    ser.close()
    producer.close()
    enter = input('Press ENTER to close producer')
    if enter == '':
    
        sys.exit('Closing Producer Client')
        time.sleep(1)

