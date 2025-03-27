# Smart-Watering-System
> Website for our MyScience Project "Smart Watering System for indoor plants"

## Components you need to build this project:
You can either order them at AliExpress or Amazon
- ESP32
- ili9341 Display
- Magnet valves and hoses
- Transistors (The ESP32 Pins do not provide enough power to run the valves)
- Hygrometer

## 3D Printing
The 3D files can be found in the STL folder. You may need to seal the water tank with some tape as some 3D printers cannot print it perfectly tight. Make sure you print the water tank with waterproof filament such as PETG. 

## ESP32 Code
The files for the ESP32 are located in the ESP32_Code folder. You can upload them to the ESP32 by using VS Code with Pymakr. Make sure you have installed MicroPython on the ESP first, otherwise it won't work. To use the iOS App make sure you have changed the WiFi settings in config.py.

## iOS App
The files for the iOS Application are in the iOS_App folder. You can open them with Xcode on MacOS and upload them to your iPhone. In the iOS App you must enter the local IP Address of the ESP32.
