/*
============================================================================
title: ESP32_BME280_LoRa_Transmitter
description: ESP32 reads weather data from BME280 sensor and them via LoRa.
author: Niklas Felhauer
GitHub: NiklasFelhauer
organization: NF-codes
date: 12/21/2020
version: 0.0
notes:
platformio_version: 5.0.4
============================================================================
*/

#include <Arduino.h>
#include <SPI.h>
#include <Adafruit_BME280.h>
#include <Adafruit_Sensor.h>
#include <LoRa.h>
#include <Wire.h>

//deep sleep settings
#define microseconds_to_seconds 1000000
#define seconds_to_minutes 60
#define TimetoSleep 10

Adafruit_BME280 bme;

//define LoRa tranceiver pins (SPI)
#define ss 5
#define rst 14
#define dio0 2

float temperature;
float humidity;
float pressure;

//===== VOID SETUP =====================================================================

void setup() {
  

  Serial.begin(115200);
  while(!Serial);
  Serial.println(F("searching for BME280 sensor"));

    //while BME280 sensor is connected incorrectly
    while (!bme.begin(0x76) ){
      Serial.print("please check BME280 sensor wiring!\n");
      delay(1000);
   }

  Serial.println(F("searching for LoRa tranceiver module"));
  LoRa.setPins(ss,rst,dio0);

  

    //while LoRa tranceiver is connected incorrectly
    //433E6 for 433 MHz (Asia)
    //866E6 for 868 MHz (Europe)
    //915E6 for 915 MHz (America)
    while (!LoRa.begin(868E6)){
      Serial.print(".");
      delay(500);
    }

  //Sync word assures you don't get LoRa messages from other LoRa tranceivers
  //Sync words of receiver and transmitter have to match
  //chose in range of 0 - 0xFF
  LoRa.setSyncWord(0xF3); 
                           

  Serial.println("\n>> initialization complete <<\n");

  //wake up esp with timer (here: after 10 minutes)
  esp_sleep_enable_timer_wakeup(TimetoSleep * microseconds_to_seconds * seconds_to_minutes);

}

//===== VOID LOOP =====================================================================

void loop() { 
  
  //get temperature
  temperature = bme.readTemperature();
  Serial.printf("Temperature = %.2f *C \n", temperature);
  
  //get pressure
  pressure = bme.readPressure() / 100.0;
  Serial.printf("Pressure = %.2f hPa \n", pressure);

  //get humidity
  humidity = bme.readHumidity();
  Serial.printf("Humidity = %.2f %% \n \n", humidity);
  
  //create LoRa Packet and send it, don't forget to close it again
  LoRa.beginPacket();
    LoRa.print(temperature);
    LoRa.print(";");
    LoRa.print(pressure); 
    LoRa.print(";");
    LoRa.print(humidity);
    LoRa.print(";");
    LoRa.flush();
  LoRa.endPacket();

  //start deep sleep to safe batterie
  esp_deep_sleep_start();
}
//===== END VOID LOOP ===================================================================
