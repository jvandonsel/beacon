import urequests

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

def is_rain(code):
    return code in RAIN_CODES

def is_snow(code):
    return code in SNOW_CODES

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
