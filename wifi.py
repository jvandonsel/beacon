import webrepl
import network
import utils
import time

def start_network():

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    ssid, password = utils.read_wifi_info_from_nvs()
    wlan.connect(ssid, password)

    # Wait for network connection
    while wlan.ifconfig()[0] == '0.0.0.0':
        print("Waiting for network...")
        time.sleep(0.250)
        utils.check_for_prompt()

    print(f"WiFi connected to ssid {ssid}, IP={wlan.ifconfig()[0]}")

    # Start the WebREPL
    webrepl.start()