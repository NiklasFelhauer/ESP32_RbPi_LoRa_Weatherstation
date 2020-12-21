# ESP32_RbPi_LoRa_Weatherstation

hey everyone!

components used: >1xESP32; >1xRaspberry Pi 4 Modell B; >1xBME280 weather sensor; >2xLoRa RFM95 tranceivers

IDE used: Visual Studio Code (Python: Microsoft Python Extension and C: PlatformIO Extension)

What is LoRa? LoRa (Long Range) is a upcoming RF technology that includes features like long range (depends highly on the area, but up to multiple miles) or low power consumption. So perfect for IoT projects like this one here!

description: ESP32 sends weather data (provided by BME280 sensor) via LoRa tranceiver to LoRa tranceiver (=connected to RbPi). Now, here are 2 directions to go: 1) RbPi sends weather data via MQTT network to NodeRed to display the data on a NodeRed dashboard OR 2) RbPi stores weather data in InflxDB (timestamps based database) to visualize the data in grafana

programming language used: mainly C (ESP32) and Python (Raspberry Pi) > (1) in NodeRed simple html, css, JAVA and JSON codes

planned updates: >3D-printed weatherstation case (I'll upload .stl data soon) >supply ESP32 with battery/solar-charger/solar-panel

more details in the specific folders.

stay tuned! :)
