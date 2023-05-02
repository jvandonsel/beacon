import json
import esp32
import uselect
import sys


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
    Checks if a serial character is present. If so, enters the interactive console.
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

