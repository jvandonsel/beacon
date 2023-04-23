###################################################################################################
# Weather Beacon
# @author Jim Van Donsel
# @since 2023/04/23
###################################################################################################

import network
import time
import urequests
import webrepl
import sys
import uselect
from machine import PWM, Pin
import json
import esp32

WEATHER_POLL_INTERVAL_SECS = 10
PROMPT_POLL_INTERVAL_SECS = 0.250

# Flash storage
NAMESPACE = "storage"
NVS_LAT_LONG_KEY = "NVS_LAT_LONG"
NVS_WIFI_KEY = "WIFI_INFO"


# LED GPIO pins
RED_GPIO = 16
BLUE_GPIO = 17
GREEN_GPIO = 21

LED_PWM_PERIOD_US = 1000
DUTY_NS_HIGH = LED_PWM_PERIOD_US * 1000

# WMO weather codes. See https://open-meteo.com/en/docs
class WeatherCode:
    SUNNY = 0
    MAINLY_SUNNY = 1
    PARTLY_CLOUDY = 2
    CLOUDY = 3
    FOGGY = 45
    FOGGY2 = 48
    LIGHT_DRIZZLE = 51
    DRIZZLE = 53
    HEAVY_DRIZZLE = 55
    LIGHT_FREEZING_DRIZZLE = 56
    FREEZING_DRIZZLE = 57
    LIGHT_RAIN = 61
    RAIN = 63
    HEAVY_RAIN = 65
    FREEZING_RAIN = 66
    FREEZING_RAIN2 = 67
    LIGHT_SNOW = 71
    SNOW = 73
    HEAVY_SNOW = 75
    SNOW_GRAINS = 77
    LIGHT_SHOWERS = 80
    SHOWERS = 81
    HEAVY_SHOWERS = 82
    SNOW_SHOWERS = 85
    SNOW_SHOWERS2 = 86
    THUNDERSTORM = 95
    THUNDERSTORM_WITH_HAIL = 96
    THUNDERSTORM_WITH_HAIL2 = 99

RAIN_CODES = {
    WeatherCode.LIGHT_DRIZZLE,
    WeatherCode.DRIZZLE,
    WeatherCode.HEAVY_DRIZZLE,
    WeatherCode.LIGHT_FREEZING_DRIZZLE,
    WeatherCode.FREEZING_DRIZZLE,
    WeatherCode.LIGHT_RAIN,
    WeatherCode.RAIN,
    WeatherCode.HEAVY_RAIN,
    WeatherCode.FREEZING_RAIN,
    WeatherCode.FREEZING_RAIN2,
    WeatherCode.LIGHT_SHOWERS,
    WeatherCode.SHOWERS,
    WeatherCode.HEAVY_SHOWERS,
    WeatherCode.SNOW_SHOWERS,
    WeatherCode.SNOW_SHOWERS2,
    WeatherCode.THUNDERSTORM,
    WeatherCode.THUNDERSTORM_WITH_HAIL,
    WeatherCode.THUNDERSTORM_WITH_HAIL2
}

SNOW_CODES = {
    WeatherCode.LIGHT_SNOW,
    WeatherCode.SNOW,
    WeatherCode.HEAVY_SNOW,
    WeatherCode.SNOW_GRAINS,
    WeatherCode.SNOW_SHOWERS,
    WeatherCode.SNOW_SHOWERS2
}

class PwmPins:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

class RGB:
    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b
    

WHITE = RGB(0xFF, 0xFF, 0xFF)
RED   = RGB(0xFF, 0, 0)
GREEN = RGB(0, 0xFF, 0)
BLLUE = RGB(0, 0, 0xFF)

def is_rain(code):
    return code in RAIN_CODES

def is_snow(code):
    return code in SNOW_CODES


def console():
    """
    Run an interactive console. Returns only on 'quit' or 'exit'
    """
    print("Entering interactive console. Weather polling is stopped. To resume, type 'quit'.")
    while True:
        cmd = input("beacon> ")
        if cmd == "":
            pass
        elif cmd == "about":
            latitude, longitude = read_location_from_nvs()
            ssid, password = read_wifi_info_from_nvs()
            print("Weather Beacon, built by Jim Van Donsel, 2023 AD")
            print("Configuration:")
            print("   Latitude: ", latitude)
            print("   Longitude: ", longitude)
            print("   SSID: ", ssid)
        elif cmd == "wifi":
            print("Set WiFi configuration")
            try:
                ssid = input("Enter SSID: ")
                password = input("Enter password: ")
                save_wifi_info_to_nvs(ssid, password)
                print('Saved.')
            except Exception as e:
                print("Failed saving: ", e)
        elif cmd == "location":
            print("Set location:")
            try:
                latitude = input("Enter latitude: ")
                longitude = input("Enter longitude: ")
                save_location_to_nvs(float(latitude), float(longitude))
                print('Saved.')
            except Exception as e:
                print("Failed saving: ", e)
        
        elif cmd == "help":
            print("Commands: ")
            print("     about     -     Show info about this device")
            print("     wifi      -     Set WiFi username, password")
            print("     location  -     Set location latitude, longitude")
            print()
        elif cmd == "quit" or cmd == "exit":
            # Empty the keyboard input buffer
            while read_one_char():
                pass
            print("Resuming weather polling.")
            return
        else:
            print("Unrecognized command")

def read_one_char():
    return(sys.stdin.read(1) if spoll.poll(0) else None)

def get_weather_code(url):
    """
    Queries the weather API for the current weather for the current location.
    Returns the numeric WMO weather code. Returns -1 it not found.
    """
    resp = {}
    code = -1
    try:
        resp = urequests.get(url)
        print("status=:", resp.status_code)
        code = resp.json()['daily']['weathercode'][0]
    except Exception as e:
        print("Caught error querying weather API:", e)
    finally:
        # Micropython is very unhappy if you don't close responses
        if resp != {}:
            resp.close()
    return code

def check_for_prompt():
    """
    Checks if a serial character is present. If so, enters the interactive console.
    """
    if read_one_char():
            console()

def init_pwm(pin, duty):
    pwm = PWM(Pin(pin))
    freq = int(1000000.0/LED_PWM_PERIOD_US)
    duty_ns =  LED_PWM_PERIOD_US * duty * 1000
    print("Setting pin " , pin, " to freq=", freq, " duty_ns=", duty_ns)
    pwm.init(freq=int(freq), duty_ns=int(duty_ns))
    return pwm


def breathe(pwms, stop_on_key_press=False):
    duty_ns = DUTY_NS_HIGH
    direction = -1
    while not (stop_on_key_press and read_one_char()):
        pwms.red.duty_ns(duty_ns)
        pwms.green.duty_ns(duty_ns)
        pwms.blue.duty_ns(duty_ns)
        duty_ns += 10000 * direction
        if duty_ns < 0:
            direction = 1
            duty_ns = 0
        if duty_ns >= DUTY_NS_HIGH:
            direction = -1
            duty_ns = DUTY_NS_HIGH
        time.sleep(0.01)


def solid(pwm, duty):
    """
    Sets the given pwm pin to the given duty cycle.
    @param pwm PWM pin
    @param duty float 0.0-1.0
    """
    pwm.duty_ns(int(DUTY_NS_HIGH * duty))

def solid_rgb(pwms, rgb):
    solid(pwms.red, rgb.red / 255.0)
    solid(pwms.green, rgb.green / 255.0)
    solid(pwms.blue, rgb.blue / 255.0)
    
def save_location_to_nvs(latitude, longitude):
    """
    Save latitude/longitude values to non-volatile storage.
    @param latitude Latitude (float)
    @param longitude Longitude (float)
    """
    nvs = esp32.NVS(NAMESPACE)
    map = {"latitude": latitude, "longitude": longitude}
    nvs.set_blob(NVS_LAT_LONG_KEY, json.dumps(map))
    nvs.commit()


def read_location_from_nvs():
    """
    Loads the latitude/longitude from non-volatile storage.
    @return (latitude, longitude) as floats, or (0,0) if not present
    """
    try:
        nvs = esp32.NVS(NAMESPACE)
        buff = bytearray(100)
        nvs.get_blob(NVS_LAT_LONG_KEY, buff)
        map = json.loads(buff.decode('utf8'))
        return (float(map['latitude']), float(map['longitude']))
    except:
        return (0,0)

def save_wifi_info_to_nvs(ssid, password):
    """
    Saves WiFi SSID and password to non-volatile storage.
    @param ssid SSID string
    @param password Password string
    """
    nvs = esp32.NVS(NAMESPACE)
    map = {"ssid": ssid, "password": password}
    nvs.set_blob(NVS_WIFI_KEY, json.dumps(map).encode('utf-8'))
    nvs.commit()

def read_wifi_info_from_nvs():
    """
    Loads WiFi SSID and password from non-volatile storage.
    @return (ssid, password), or ('', '') if not present
    """
    try:
        nvs = esp32.NVS(NAMESPACE)
        buff = bytearray(100)
        nvs.get_blob(NVS_WIFI_KEY, buff)
        map = json.loads(buff.decode('utf8'))
        return (map['ssid'], map['password'])
    except:
        return ('', '')


def get_weather_url(latitude, longitude):
    return f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode&timezone=auto&forecast_days=1"

###################################################################################################
# Main
###################################################################################################

# Configure non-blocking serial reads
spoll=uselect.poll()
spoll.register(sys.stdin,uselect.POLLIN)

# Configure network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid, password = read_wifi_info_from_nvs()
print(">>>Read ssid=", ssid, " password=", password)

latitude, longitude = read_location_from_nvs()
print(">>>read lat=", latitude, "longitude=", longitude)

wlan.connect(ssid, password)

# Wait for network connection
while wlan.ifconfig()[0] == '0.0.0.0':
    print("Waiting for network...")
    time.sleep(0.250)
    check_for_prompt()

print("WiFi connected, IP=", wlan.ifconfig()[0])

# Start the WebREPL
webrepl.start()

# Create PWM pings
pwms = PwmPins(init_pwm(RED_GPIO, 1.0), init_pwm(GREEN_GPIO, 1.0), init_pwm(BLUE_GPIO, 1.0))


solid_rgb(pwms, WHITE)

# breathe(pwms, WHITE)

url = get_weather_url(latitude, longitude)

while True:
    code = get_weather_code(url)
    print("weather code =", code)
    if is_rain(code):
        print("RAIN!")
    elif is_snow(code):
        print("SNOW")

    # Continually check for an input keystroke and enter the interactive console if found.  
    # In a perfect world we would put the interactive console and the weather monitor in separate
    # threads, but MicroPython's threads are pretty broken and don't work with networking.
    # the 
    for i in range(int(WEATHER_POLL_INTERVAL_SECS/PROMPT_POLL_INTERVAL_SECS)):
        check_for_prompt()
        time.sleep(PROMPT_POLL_INTERVAL_SECS)



