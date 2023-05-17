import json
import esp32
import uselect
import wifi
import sys
import ntptime
import time


# Flash storage
NAMESPACE = "storage"
NVS_LAT_LONG_KEY = "NVS_LAT_LONG"
NVS_WIFI_KEY = "WIFI_INFO"

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
            print("   Wifi Connected?",  wifi.is_connected)

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
        
        elif cmd == "help" or cmd == "?":
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


# Configure non-blocking serial reads
spoll=uselect.poll()
spoll.register(sys.stdin,uselect.POLLIN)

def read_one_char():
    # type: () -> str
    """
    Reads a single character from the serial console.
    @return The character read, or None if no character was read.
    """
    return(sys.stdin.read(1) if spoll.poll(0) else None)

def check_for_prompt():
    # type: () -> None
    """
    Checks if a serial character is present. If so, enters the interactive console,
    which then blocks until it' exited.
    """
    if read_one_char():
            console()

def save_location_to_nvs(latitude, longitude):
    # type: (float, float) -> None
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
    # type:  () -> (float, float)
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
    # type:  (str, str) -> None
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
    # type:  () -> (str, str)
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
    
def sync_ntp():
    """
    Sync our local clock to an NTP server
    """
    # Try a few times. Micropython NTP library is not very reliable.
    for i in range(5):
        try:
            ntptime.settime()
            print("Successfully got NTP  time")
            break
        except Exception as e:
            print("Failed to get NTP time:", e)
            time.sleep(10)

def get_local_time(utc_offset):
    # type:  (int) -> (int, int)
    """
    @param utc_offset Offset from UTC in hours
    @return (hour,minute) of local time
    """
    (h, m) = get_utc_time()
    if h == None:
        # NTP is flaky in micropython, so try to ride through it
        h = 0
    return (int((h + utc_offset) % 24), m)
    
def get_utc_time():
    # type:  () -> (int, int)
    """
    Return the current hours and minutes in UTC time.
    @return (hours, minutes)
    """
    hours = time.localtime()[3]
    minutes = time.localtime()[4]
    return (hours, minutes)