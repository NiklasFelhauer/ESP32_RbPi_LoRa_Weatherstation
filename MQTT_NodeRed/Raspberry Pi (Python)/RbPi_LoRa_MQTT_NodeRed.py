#===============================================================================
#title: RbPi_LoRa_MQTT_NodeRed.py
#description: send weather data to NodeRed with MQTT
#NodeRed dashboard: http://localhost:8086
#author: Niklas Felhauer
#GitHub: https://github.com/NiklasFelhauer
#organization: NF-codes
#date: 12/10/2020
#version 0.0
#notes: BETA
#python_version:3.7.3
#===============================================================================

from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
import paho.mqtt.publish as publish

MQTT_SERVER = "192.168.43.188"
MQTT_TOPIC = "/esp32/weather"

BOARD.setup()



class MyLoRaClass(LoRa):
    def __init__(self, verbose=False):
        super(MyLoRaClass, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)
        self.set_freq(868.0)
        self.set_sync_word(0xF3)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT) 
        while True:
            sleep(10)
            payload = self.read_payload(nocheck=True)
            sys.stdout.flush()
            payload_data = bytes(payload).decode("utf-8", 'ignore')          
            if len(payload_data) == 16:
                print(payload_data)
                previous_payload_data = payload_data


            else:
                payload_data = previous_payload_data
                print(previous_payload_data)
                print("ERROR ABOTH")
            self.clear_irq_flags(RxDone=1)
            self.set_mode(MODE.SLEEP)
            self.reset_ptr_rx()

            
            self.set_mode(MODE.RXCONT) 
            publish.single("/esp32/weather", payload_data, hostname=MQTT_SERVER)
            #publish.single("/esp32/weather/pressure", pressure, hostname=MQTT_SERVER)
            #publish.single("/esp32/weather/humidity", humidity, hostname=MQTT_SERVER)
            
            
            

lora = MyLoRaClass(verbose=False)

try:
    lora.start()
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
    
