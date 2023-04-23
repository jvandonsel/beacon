###################################################################################################
# Weather Beacon for ESP32
# @author Jim Van Donsel
# @since 2023/04/23
###################################################################################################

import network
import time
import urequests
import webrepl
from machine import PWM, Pin
import utils
import weather

WEATHER_POLL_INTERVAL_SECS = 10
PROMPT_POLL_INTERVAL_SECS = 0.250


# LED GPIO pins
RED_GPIO = 16
BLUE_GPIO = 17
GREEN_GPIO = 21

LED_PWM_PERIOD_US = 1000
DUTY_NS_HIGH = LED_PWM_PERIOD_US * 1000

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
    

def get_weather_url(latitude, longitude):
    return f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode&timezone=auto&forecast_days=1"

###################################################################################################
# Main
###################################################################################################

# Configure network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

ssid, password = utils.read_wifi_info_from_nvs()
print(">>>Read ssid=", ssid, " password=", password)

latitude, longitude = utils.read_location_from_nvs()
print(">>>read lat=", latitude, "longitude=", longitude)

wlan.connect(ssid, password)

# Wait for network connection
while wlan.ifconfig()[0] == '0.0.0.0':
    print("Waiting for network...")
    time.sleep(0.250)
    utils.check_for_prompt()

print("WiFi connected, IP=", wlan.ifconfig()[0])

# Start the WebREPL
webrepl.start()

# Create PWM pings
pwms = PwmPins(init_pwm(RED_GPIO, 1.0), init_pwm(GREEN_GPIO, 1.0), init_pwm(BLUE_GPIO, 1.0))


solid_rgb(pwms, WHITE)

# breathe(pwms, WHITE)

url = get_weather_url(latitude, longitude)

while True:
    code = weather.get_weather_code(url)
    print("weather code =", code)
    if weather.is_rain(code):
        print("RAIN!")
    elif weather.is_snow(code):
        print("SNOW")

    # Continually check for an input keystroke and enter the interactive console if found.  
    # In a perfect world we would put the interactive console and the weather monitor in separate
    # threads, but MicroPython's threads are pretty broken and don't work with networking.
    # the 
    for i in range(int(WEATHER_POLL_INTERVAL_SECS/PROMPT_POLL_INTERVAL_SECS)):
        utils.check_for_prompt()
        time.sleep(PROMPT_POLL_INTERVAL_SECS)



