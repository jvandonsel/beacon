###################################################################################################
# Weather Beacon for ESP32
# @author Jim Van Donsel
# @since 2023/04/23
###################################################################################################

import utils
import led
import weather
import wifi

def weather_to_color(w):
    # type: (weather.WeatherValue) -> [led.RGB, bool)
    """
    Given a WeatherValue, determine the color and pattern.
    @return (RGB, pulse) RGB: color to display, pulse: if True, pulse, else solid.
    """
    if w == weather.WeatherValue.SUN:
        return led.BLUE, False
    if w == weather.WeatherValue.CLOUDS:
        return led.BLUE, True
    if w == weather.WeatherValue.RAIN:
        return led.RED, False
    if w == weather.WeatherValue.SNOW:
        return led.RED, True
    if w == weather.WeatherValue.FOG:
        return led.GREEN, True
    
    # not found
    return led.WHITE, False

# Create PWM pins
pwmPins = led.create_pwm_pins()

# Color during startup
led.solid_rgb(pwmPins, led.MAGNENTA)

# Start the WiFi network. Will block until a wifi network is found, 
# or until a key is hit.
wifi.start_network()

# Display white until we get the weather
led.solid_rgb(pwmPins, led.WHITE)

# Read our location from NVS
latitude, longitude = utils.read_location_from_nvs()
print("Read lat=", latitude, "longitude=", longitude)

WEATHER_POLL_INTERVAL_SECS = 3600

while True:
    wv = weather.query_weather(latitude, longitude)
    color, pulse = weather_to_color(wv)
    print("Weather:", weather.WeatherValue.to_string(wv), " color:", color.to_str(), ", pulse:", pulse)

    # Display an LED pattern based on the weather value. These calls block until a serial character is received
    # or until the time interval has expired.
    result = 0
    if pulse:
        result = led.breathe_wait(pwmPins, color, WEATHER_POLL_INTERVAL_SECS)
    else:
        result = led.solid_wait(pwmPins, color, WEATHER_POLL_INTERVAL_SECS)

    if result == 1:
        # Key was hit, enter console. Blocks until the user types 'exit' or reboots.
        utils.console()


    

