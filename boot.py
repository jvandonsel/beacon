###################################################################################################
# Weather Beacon for ESP32 in Micropython
# @author Jim Van Donsel
# @since 2023/04/23
###################################################################################################

import utils
import leds
import weather
import wifi

def weather_to_color(w):
    # type: (weather.WeatherValue) -> (leds.RGB, bool)
    """
    Given a WeatherValue, determine the color and pattern.
    @return (RGB, pulse) RGB: color to display, pulse: if True, pulse, else solid.
    """
    if w == weather.WeatherValue.SUN:
        return leds.BLUE, False
    if w == weather.WeatherValue.CLOUDS or w == weather.WeatherValue.FOG:
        return leds.BLUE, True
    if w == weather.WeatherValue.RAIN:
        return leds.RED, False
    if w == weather.WeatherValue.THUNDERSTORM:
        return leds.RED, True
    if w == weather.WeatherValue.SNOW:
        return leds.RED, True
    
    # not found
    return leds.WHITE, False

# Create PWM pins
pwmPins = leds.create_pwm_pins()

# Color during startup
leds.solid_rgb(pwmPins, leds.MAGNENTA)

# Start the WiFi network. Will block until a wifi network is found, 
# or until a key is hit.
wifi.start_network()

# Display white until we get the weather
leds.solid_rgb(pwmPins, leds.WHITE)

# Read our location from NVS
latitude, longitude = utils.read_location_from_nvs()
print("Read lat=", latitude, "longitude=", longitude)

WEATHER_POLL_INTERVAL_SECS = 900

# Sync NTP
utils.sync_ntp()

daily_ntp_sync_done = True

while True:

    # Check the weather
    wv = weather.query_weather_value(latitude, longitude)
    color, pulse = weather_to_color(wv)
    print("Weather:", weather.WeatherValue.to_string(wv), " color:", color.to_str(), ", pulse:", pulse)
    
    # Get the local time
    (local_hour, local_minute) = utils.get_local_time(weather.get_utc_offset_hours())
    print(f"Local time: {str(local_hour)}:{str(local_minute)}")

    # Sync to NTP daily, since our clock is prone to drift
    if local_hour == 0:
        daily_ntp_sync_done = False
    if local_hour == 1 and not daily_ntp_sync_done:
        utils.sync_ntp()
        daily_ntp_sync_done = True

    # Go to nightlight mode if it's very late
    if local_hour <= 6 or local_hour >= 23:
        result = leds.solid_wait(pwmPins, leds.WHITE, WEATHER_POLL_INTERVAL_SECS, 0.05)
    else:
        # Display an LED pattern based on the weather value. These calls block until a serial character is received
        # or until the time interval has expired.
        result = 0
        if pulse:
            result = leds.breathe_wait(pwmPins, color, WEATHER_POLL_INTERVAL_SECS)
        else:
            result = leds.solid_wait(pwmPins, color, WEATHER_POLL_INTERVAL_SECS)

        if result == 1:
            # Key was hit, enter console. Blocks until the user types 'exit' or reboots.
            utils.console()


    

