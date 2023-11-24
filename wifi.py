import webrepl
import network
import utils
import time

is_connected = False

def start_network():
    # type: () -> None
    """
    Connect to the WiFi network with credentials read from NVS.
    Also starts WebREPL.
    """

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
    global is_connected
    is_connected = True

    # Start the WebREPL
    webrepl.start()

def get_ip():
    wlan = network.WLAN(network.STA_IF)
    return wlan.ifconfig()[0]
