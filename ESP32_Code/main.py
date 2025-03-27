# boot.py -- run on boot-up
from time import sleep, time, localtime
from ili9341 import color565
from machine import Pin, ADC
import socket
import _thread
import json

# Attribute definieren für Hygrometer-ESP32-Magnetventile
ventil1 = Pin(19, Pin.OUT)
ventil2 = Pin(18, Pin.OUT)

# Methoden definieren für Hygrometer-ESP32-Magnetventile
def ventil_aus(ventil):
    if ventil == 1:
        ventil1.value(1)
        display.fill_rectangle(175, 265, 50, 50, 0)
        display.draw_image("watering-complete.raw", 180, 275, 40, 40)
        print("Ventil 1 aus")
    else:
        ventil2.value(1)
        display.fill_rectangle(175, 110, 50, 50, 0)
        display.draw_image("watering-complete.raw", 180, 120, 40, 40)
        print("Ventil 2 aus")

def ventil_an(ventil):
    if ventil == 1:
        ventil1.value(0)
        display.draw_image("watering-can.raw", 175, 265, 50, 50)
        print("Ventil 1 an")
    else:
        ventil2.value(0)
        display.draw_image("watering-can.raw", 175, 110, 50, 50)
        print("Ventil 2 an")

ventil_aus(1)
ventil_aus(2)

# Initialisiere den analogen Eingang für Pflanze 1
adc1 = ADC(Pin(35))  # Verbinde den AO-Pin des Sensors mit GPIO34
adc1.atten(ADC.ATTN_11DB)  # Konfiguriert den ADC für eine Eingangsreichweite von 0-3.3V
adc1.width(ADC.WIDTH_12BIT)  # 12-Bit-Auflösung (0-4095)

# Initialisiere den analogen Eingang für Pflanze 2
adc2 = ADC(Pin(34))  # Verbinde den AO-Pin des Sensors mit GPIO34
adc2.atten(ADC.ATTN_11DB)  # Konfiguriert den ADC für eine Eingangsreichweite von 0-3.3V
adc2.width(ADC.WIDTH_12BIT)  # 12-Bit-Auflösung (0-4095)

# globale Variablen 
local_time = None
zul_bewaessert1 = "noch nicht"
zul_bewaessert2 = "noch nicht"

# Lade gespeicherte Konfiguration
def load_saved_values():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config
    except:
        return {
            "plant1": {
                "name": "Pflanze 1",
                "threshold": 20,
                "watering_duration": 50
            },
            "plant2": {
                "name": "Pflanze 2",
                "threshold": 20,
                "watering_duration": 50
            },
            "summertime": False
        }

config = load_saved_values()
name1 = config["plant1"]["name"]
name2 = config["plant2"]["name"]
schwellwert1 = config["plant1"]["threshold"]
schwellwert2 = config["plant2"]["threshold"]
wasserdauer1 = config["plant1"]["watering_duration"]
wasserdauer2 = config["plant2"]["watering_duration"]
SOMMERZEIT = config["summertime"]

# Speichere aktuelle Konfiguration
def save_values():
    config = {
        "plant1": {
            "name": name1,
            "threshold": schwellwert1,
            "watering_duration": wasserdauer1
        },
        "plant2": {
            "name": name2,
            "threshold": schwellwert2,
            "watering_duration": wasserdauer2
        },
        "summertime": SOMMERZEIT
    }
    with open('config.json', 'w') as f:
        json.dump(config, f)

def bewaessern(pflanze):
    global zul_bewaessert1, zul_bewaessert2
    updateTime()
    if pflanze == 1:
        ventil_an(1)
        sleep(wasserdauer1*60/15)
        ventil_aus(1)
        zul_bewaessert1 = format_time(local_time)
    else:
        ventil_an(2)
        sleep(wasserdauer2*60/15)
        ventil_aus(2)
        zul_bewaessert2 = format_time(local_time)
    sleep(30)
    display.fill_rectangle(175, 0, 50, 320, 0)

# Zeitzonen-Korrektur
WINTERZEIT_OFFSET = 1 * 3600  # 1 Stunde in Sekunden (UTC+1)
SOMMERZEIT_OFFSET = 2 * 3600  # 2 Stunden in Sekunden (UTC+2)

def updateTime():
    global local_time
    # Aktuelle UTC-Zeit holen
    timestamp = time()

    # Manuelle Zeitzonenanpassung
    if SOMMERZEIT == True:
        corrected_time = timestamp + SOMMERZEIT_OFFSET
    elif SOMMERZEIT == False:
        corrected_time = timestamp + WINTERZEIT_OFFSET
    else:
        print("Ungültiger ZEITMODUS. Standardmäßig UTC verwenden.")
        corrected_time = timestamp
    # In lokale Zeit umwandeln
    local_time = localtime(corrected_time)

# Funktion zum Formatieren der Uhrzeit
def format_time(tm):
    return f"{tm[2]:02d}.{tm[1]:02d}. {tm[3]:02d}:{tm[4]:02d}"

# Server-Thread-Funktion
def start_server():
    global name1, name2, schwellwert1, schwellwert2, wasserdauer1, wasserdauer2, SOMMERZEIT

    addr = ('', 80)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Web server running...")

    while True:
        try:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            request = conn.recv(1024).decode()

            updateTime()

            # Verarbeite GET-Anfragen
            if "GET /api" in request:
                data = {
                    "plant1": {
                        "name": name1,
                        "humidity": round(prozent1, 2),
                        "last_watered": zul_bewaessert1,
                        "threshold": schwellwert1,
                        "watering_duration": wasserdauer1
                    },
                    "plant2": {
                        "name": name2,
                        "humidity": round(prozent2, 2),
                        "last_watered": zul_bewaessert2,
                        "threshold": schwellwert2,
                        "watering_duration": wasserdauer2
                    },
                    "summertime": SOMMERZEIT,
                    "last_update": format_time(local_time)
                    
                }
                response = json.dumps(data)
                conn.send("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n")
                conn.send(response)

            # Verarbeite POST-Anfragen
            elif "POST /api" in request: 
                content_length = int(request.split("Content-Length: ")[1].split("\r\n")[0])
                body = request[-content_length:]
                received_data = json.loads(body)

                # Aktualisiere Werte
                if "plant1" in received_data:
                    name1 = received_data["plant1"].get("name", name1)
                    schwellwert1 = received_data["plant1"].get("threshold", schwellwert1)
                    wasserdauer1 = received_data["plant1"].get("watering_duration", wasserdauer1)
                  
                if "plant2" in received_data:
                    name2 = received_data["plant2"].get("name", name2)
                    schwellwert2 = received_data["plant2"].get("threshold", schwellwert2)
                    wasserdauer2 = received_data["plant2"].get("watering_duration", wasserdauer2)
                    
                if "summertime" in received_data:
                    SOMMERZEIT = received_data["summertime"]  # Aktualisiere Sommerzeit
                
                if "watering" in received_data:
                        print("watering received")
                        plantID = received_data["watering"].get("plant")
                        bewaessern(plantID)

                # Speichere neue Konfiguration
                save_values()
                conn.send("HTTP/1.1 200 OK\r\n\r\nEinstellungen aktualisiert.")
                print(f"Einstellungen aktualisiert: {received_data}")

            else:
                conn.send("HTTP/1.1 404 Not Found\r\n\r\n")

            conn.close()
        except Exception as e:
            print(f"Fehler: {e}")
        
# Starte den Server in einem separaten Thread
_thread.start_new_thread(start_server, ())

display.clear()
display.draw_text(230, 320, f'IPv4: {ip}', bally,
                color565(70, 145, 90),
                landscape=True)

#Hauptprogramm
while True:
    feuchtigkeit1 = adc1.read()  # Lies den ADC-Wert (0 bis 4095)
    feuchtigkeit2 = adc2.read()
    
    # Konvertiere den ADC-Wert in eine Spannung
    spannung1 = feuchtigkeit1 * 3.3 / 4095  # Konvertiere in Volt (0-3.3V)
    spannung2 = feuchtigkeit2 * 3.3 / 4095  # Konvertiere in Volt (0-3.3V)
    
    # Konvertiere die Spannung in einen prozentualen Feuchtigkeitswert
    prozent1 = (3.3 - spannung1) / 3.3 * 100  # 0V = 100%, 3.3V = 0%
    prozent2 = (3.3 - spannung2) / 3.3 * 100  # 0V = 100%, 3.3V = 0%

    #Displayinhalt löschen
    display.fill_rectangle(0, 0, 174, 320, 0)

    # Ausgabe Pflanze1
    print(f"Pflanze1: {prozent1:.2f}%")

    display.draw_text(0, 320, f'{name1}', unispace,
                    color565(255, 255, 255),
                    landscape=True)
    
    display.draw_text(30, 320, 'Feuchtigkeit:', bally,
                    color565(255, 255, 255),
                    landscape=True)
    
    if prozent1 > 50:
        display.draw_text(39, 320, f'{prozent1:.1f}%', unispace,
                      color565(0, 255, 0),
                      landscape=True)
    elif prozent1 > schwellwert1:
        display.draw_text(39, 320, f'{prozent1:.1f}%', unispace,
                      color565(255, 165, 0),
                      landscape=True)
    else:
        display.draw_text(39, 320, f'{prozent1:.1f}%', unispace,
                      color565(255, 0, 0),
                      landscape=True)
        
    display.draw_text(66, 320, 'zul. bewaessert:', bally,
                    color565(255, 255, 255),
                    landscape=True)

    display.draw_text(75, 320, f'{zul_bewaessert1}', unispace,
                    color565(255, 255, 255),
                    landscape=True)

    display.draw_text(105, 320, 'Schwellwert:', bally,
                    color565(255, 255, 255),
                    landscape=True)

    display.draw_text(114, 320, f'{schwellwert1}%', unispace,
                    color565(255, 255, 255),
                    landscape=True)

    display.draw_text(141, 320, 'Wassermenge:', bally,
                    color565(255, 255, 255),
                    landscape=True)

    display.draw_text(150, 320, f'{wasserdauer1} ml', unispace,
                    color565(255, 255, 255),
                    landscape=True)

    # Ausgabe Pflanze2
    print(f"Pflanze2: {prozent2:.2f}%")

    display.draw_text(0, 160, f'{name2}', unispace,
                    color565(255, 255, 255),
                    landscape=True)
    
    display.draw_text(30, 160, 'Feuchtigkeit:', bally,
                    color565(255, 255, 255),
                    landscape=True)

    if prozent2 > 50:
        display.draw_text(39, 160, f'{prozent2:.1f}%', unispace,
                      color565(0, 255, 0),
                      landscape=True)
    elif prozent2 > schwellwert2:
        display.draw_text(39, 160, f'{prozent2:.1f}%', unispace,
                      color565(255, 165, 0),
                      landscape=True)
    else:
        display.draw_text(39, 160, f'{prozent2:.1f}%', unispace,
                      color565(255, 0, 0),
                      landscape=True)
        
    display.draw_text(66, 160, 'zul. bewaessert:', bally,
                    color565(255, 255, 255),
                    landscape=True)

    display.draw_text(75, 160, f'{zul_bewaessert2}', unispace,
                    color565(255, 255, 255),
                    landscape=True)

    display.draw_text(105, 160, 'Schwellwert:', bally,
                    color565(255, 255, 255),
                    landscape=True)

    display.draw_text(114, 160, f'{schwellwert2}%', unispace,
                    color565(255, 255, 255),
                    landscape=True)

    display.draw_text(141, 160, 'Wassermenge:', bally,
                    color565(255, 255, 255),
                    landscape=True)

    display.draw_text(150, 160, f'{wasserdauer2} ml', unispace,
                    color565(255, 255, 255),
                    landscape=True)

    # Prüfen der feuchtigkeit + ggf Bewässerung
    if prozent1 < schwellwert1:
            bewaessern(1)
    if prozent2 < schwellwert2:
            bewaessern(2)

    # Warte
    sleep(30)
