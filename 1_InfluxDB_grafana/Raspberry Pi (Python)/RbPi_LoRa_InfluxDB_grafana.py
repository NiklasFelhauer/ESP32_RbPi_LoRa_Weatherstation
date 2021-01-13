#===============================================================================
#title: RbPi_LoRa_InfluxDB_grafana.py
#description: upload data to Influx DataBase and visualize them on grafana
#             dashboard
#grafana dashboard: http://localhost:8086
#author: Niklas Felhauer
#GitHub: https://github.com/NiklasFelhauer
#organization: NF-codes
#date: 01/04/2020
#version 1.0
#notes:
#python_version:3.7.3
#===============================================================================

from SX127x.LoRa import *
from SX127x.board_config import BOARD
from influxdb import InfluxDBClient
from datetime import datetime
from time import sleep
import pytz
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%SZ',
filename='Logfile_Weather_station.log', filemode='w', level=logging.Warning) # set logging level to Warning

BOARD.setup()

#=== CLASSES & FUNCTIONS =======================================================

class GetLoRa(LoRa):    
    def __init__(self, verbose=False):
        super(GetLoRa, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_freq(868.0)     #has to match freq of transmitter: Europe: 868.0, Asia: 433.0, America: 915.0
        self.set_sync_word(0xF3) #has to match Synword of transmitter

# Function to connect to influxDB
def influxDBConnect():
    try:
        clientDB = InfluxDBClient(host = 'localhost', port = '8086') # create client object
        clientDB.create_database('Weather_Data') # create DB
        clientDB.switch_database('Weather_Data') # switch to DB
        logging.info("Connection to influxDB successful!")

    except:
        logging.error("Connection to influxDB failed!")
    finally:
        return clientDB
 
# Function to write to influxDB
def influxDBWrite(val_temp, val_hum, val_press):
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ') #time format
 
    jason_body = [
        {
        "measurement": "Sensor_data", 
        "tags": {
            #"Temperature": , Don't need tags in this example
            #"Humidity": 
        },
        "time": timestamp,
        "fields": {
            "Temperature": val_temp, #define InfluxDB fields
            "Humidity": val_hum,
            "Pressure": val_press
        }
        }
    ]
    try:
        clientDB.write_points(jason_body) # write data to DB
        logging.debug("Writing to influxDB successfull!")
    except:
        logging.error("Failure when writing to influxDB!")

def failFilter(f_temp, f_humidity, f_pressure): #filters unrealistic measurements and replaces them with presvious value(e.g. 3000°C)
    if f_temp > previous_temp + 3 or f_temp < previous_temp - 3:
        f_temp = previous_temp
    else:
        pass
    if f_humidity > previous_humidity + 10 or f_humidity < previous_humidity - 10:
        f_humidity = previous_humidity
    else:
        pass
    if f_pressure > previous_pressure + 2 or f_pressure < previous_pressure -2:
        f_pressure = previous_pressure
    else:
        pass
    return f_temp, f_humidity, f_pressure 

def firstValue():
    global switch, previous_temp, previous_humidity, previous_pressure
    if switch:
        previous_temp = temp
        previous_humidity = humidity
        previous_pressure = pressure
        switch = False
    else:
        pass

clientDB = influxDBConnect() # call function to connect to influxDB

#=== MAIN FUNCTION =============================================================
if __name__ == "__main__":
    lora = GetLoRa(verbose=False)
    lora.reset_ptr_rx()
    lora.set_mode(MODE.RXCONT) 
    previous_payload_data = 0
    switch = True
    while True:
        payload = lora.read_payload(nocheck=True) #receive LoRa packet and decode it
        sys.stdout.flush()
        payload_data = bytes(payload).decode("utf-8", 'ignore')
        try:
            if previous_payload_data != payload_data: #check if it's the right data format
                temp = float(payload_data.strip().split(";")[0]) 
                pressure = float(payload_data.strip().split(";")[1])
                humidity = float(payload_data.strip().split(";")[2])

                
                firstValue() #get first value (for failFilter function -> next function below below)

                new_temp, new_humidity, new_pressure = failFilter(temp, humidity, pressure)

                previous_temp = new_temp
                previous_humidity = new_humidity
                previous_pressure = new_pressure
                previous_payload_data = payload_data
                influxDBWrite(new_temp, new_humidity, new_pressure) #upload values to Influx database
            else:
                pass  
        except:
            logging.warning("Couldn't convert data to float")

    sys.stdout.flush()
#=== END MAIN FUNCTION ========================================================= 
