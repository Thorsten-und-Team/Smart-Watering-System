from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont
import network
import time
import ntptime

# Wi-Fi Config 
ssid = "your ssid"
password = "your password"

display = None
spi = None
unispace = None
bally = None
ip = None

# Initalisiere das Display
def displayConfig():
        global display, spi
        spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
        display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

# Fonts laden
def downloadFonts():
        global unispace, bally
        print("Downloading Fonts...")
        unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)
        bally = XglcdFont('fonts/Bally7x9.c', 7, 9)

# Connect to Network
def networkConnect():
        global ip
        station = network.WLAN(network.STA_IF)
        station.active(True)
        station.connect(ssid, password)

        i = 1
        while not station.isconnected() and i<31:
                print(f"Connecting to Wi-Fi... Versuch {i}")
                time.sleep(1)
                i=i+1

        ip = station.ifconfig()[0]

        print("Connected to Wi-Fi")
        print("IP Address:", station.ifconfig()[0])


def syncTime():
    try:
        print("Synchronisiere Uhrzeit mit NTP-Server..")
        # Zeit synchronisieren
        ntptime.host = "de.pool.ntp.org"
        ntptime.settime()
        print("Uhrzeit synchronisiert.")

    except Exception as e:
        print("Fehler bei der Zeitsynchronisation:", e)

displayConfig()
downloadFonts()
display.draw_text(108, 200, 'loading', unispace,
                color565(255, 255, 255),
                landscape=True)
display.draw_text(108, 200, 'loading.', unispace,
                color565(255, 255, 255),
                landscape=True)
time.sleep(0.5)
display.draw_text(108, 200, 'loading..', unispace,
                color565(255, 255, 255),
                landscape=True)
networkConnect()
display.draw_text(108, 200, 'loading...', unispace,
                color565(255, 255, 255),
                landscape=True)
syncTime()
