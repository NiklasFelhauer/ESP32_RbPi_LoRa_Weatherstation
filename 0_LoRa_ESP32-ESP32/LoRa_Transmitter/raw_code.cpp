/*
============================================================================
title: NodeMCU_LoRa_Transmitter
description: sends test packet with counter via LoRa
author: Niklas Felhauer
GitHub: NiklasFelhauer
organization: NF-codes
date: 12/10/2020
version: 0.0
notes: don't forget to write: monitor_speed=115200 in "platformio.ini" 
platformio_version: 5.0.4
============================================================================
*/

//include libraries
#include <Arduino.h>
#include <SPI.h>
#include <LoRa.h> //run this in the terminal to download: pio lib install "sandeepmistry/LoRa"

//define the pins used by the transceiver module
#define ss 5
#define rst 14
#define dio0 2

int counter;

//===== VOID SETUP =====================================================================

void setup() {
  //initialize Serial Monitor, don't forget to match platformio.ini settings 
  Serial.begin(115200);
  while (!Serial);
  Serial.println("LoRa Tranceiver connected correctly!");

  //setup LoRa transceiver module
  LoRa.setPins(ss, rst, dio0);
  
  //while LoRa tranceiver is connected incorrectly
  //433E6 for 433 MHz (Asia)
  //866E6 for 868 MHz (Europe)
  //915E6 for 915 MHz (America)
  while (!LoRa.begin(866E6)) {
    Serial.println(".");
    delay(500);
  }

  //Sync word assures you don't get LoRa messages from other LoRa tranceivers
  //Sync words of receiver and transmitter have to match
  //chose in range of 0 - 0xFF
  LoRa.setSyncWord(0xF4);
  Serial.println("LoRa Initializing OK!");
}

//===== VOID LOOP =====================================================================

void loop() {
  Serial.print("Sending packet: ");
  Serial.println(counter);

  //create LoRa packet
  LoRa.beginPacket();
    //here comes the content, you want to store in the packet
    LoRa.print("My message number: "); 
    LoRa.print(counter);
  //close packet
  LoRa.endPacket();

  //increase counter variable that it counts up
  counter++;

  //wait 10 sec
  delay(10000);
}

//===== END VOID LOOP ===================================================================