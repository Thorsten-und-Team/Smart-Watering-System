# Smart-Watering-System
Smart Watering System for indoor plants to 3D print

## Components you need to build this project:
You can either order them at AliExpress or Amazon
- ESP32
- ili9341 Display
- Magnet valves
- Hygrometer

## 3D Printing
The 3D files are in the STL folder. Maybe you have to seal the water tank with some ducktape, because some 3D-Printers can't print it perfectly tight. Make sure to print the water tank with waterproof filament like PETG. 

## ESP32 Code
The files for the ESP32 are in the ESP32_Code folder. You can upload them to the ESP32 by using VS Code with Pymakr. Make sure you have installed MicroPython on the ESP first, otherwise it won't work. To use the iOS App you have to change the WiFi settings in config.py.

## iOS App
The files for the iOS Application are in the iOS_App folder. You can open them with Xcode on MacOS and upload them to your iPhone. In the iOS App you must enter the local IP Address of the ESP32.
