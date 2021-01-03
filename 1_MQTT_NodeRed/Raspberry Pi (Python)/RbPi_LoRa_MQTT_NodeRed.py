#===============================================================================
#title: RbPi_LoRa_MQTT_NodeRed.py
#description: send weather data to NodeRed with MQTT
#NodeRed dashboard: http://localhost:8086
#author: Niklas Felhauer
#GitHub: https://github.com/NiklasFelhauer
#organization: NF-codes
#date: 12/10/2020
#version 0.1
#notes: BETA // Update not tested <<<<<<<<<
#python_version:3.7.3
#===============================================================================

from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
import paho.mqtt.publish as publish
from datetime import datetime
import pytz
import logging



logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%dT%H:%M:%SZ',
filename='Logfile_Weather_station_NodeRed.log', filemode='w', level=logging.Warning) # set logging level to Warning

MQTT_SERVER = "IP-Adresse" # put your RaspberryPi-IP in here. Command for terminal: hostname -I    //IP Adress will change Pi is connected to another WiFi
MQTT_TOPIC = "/esp32/weather" # your MQTT topic

BOARD.setup()

#=== CLASSES & FUNCTIONS =======================================================

class MyLoRa(LoRa):    
    def __init__(self, verbose=False):
        super(MyLoRa, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_freq(868.0)     #has to match freq of transmitter: Europe: 868.0, Asia: 433.0, America: 915.0
        self.set_sync_word(0xF3) #has to match Synword of transmitter

#=== MAIN FUNCTION =============================================================

if __name__ == "__name__":
    lora = MyLoRa(verbose=False)
    lora.reset_ptr_rx()
    lora.set_mode(MODE.RXCONT)
    previous_payload_data = 0
    switch = True

    while True:
        payload = lora.read_payload(nocheck=True)
        sys.stdout.flush()
        payload_data = bytes(paylaod).decode("utf-8", 'ignore')
        try:
            if previous_payload_data != payload_data: #check if it's the right data format
                temp = float(payload_data.strip().split(";")[0]) 
                pressure = float(payload_data.strip().split(";")[1])
                humidity = float(payload_data.strip().split(";")[2])

                publish.single("/esp32/weather", payload_data, hostname=MQTT_SERVER) # Publish MQTT message
            else:
                pass
            
            previous_payload_data = payload_data

        except:
            logging.Warning("Couldn't convert payload_data to float")

    sys.stdout.flush()

#=== END MAIN FUNCTION ========================================================= 