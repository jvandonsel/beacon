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


SUNNY_CODES  = {
    WeatherCode.SUNNY,
    WeatherCode.MAINLY_SUNNY
}
    

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

CLOUD_CODES = {
    WeatherCode.CLOUDY,
    WeatherCode.PARTLY_CLOUDY
}

FOG_CODES = {
    WeatherCode.FOGGY, 
    WeatherCode.FOGGY2
}

# Coarse weather classification
class WeatherValue:
    UNKNOWN = 0
    SUN = 1
    RAIN = 2
    SNOW = 3
    CLOUDS = 4
    FOG = 5

    weather_value_to_string = {
        UNKNOWN: "UNKNOWN",
        SUN: "SUN",
        RAIN: "RAIN",
        SNOW: "SNOW",
        CLOUDS: "CLOUDS",
        FOG: "FOG"
    }

    def to_string(value):
        return WeatherValue.weather_value_to_string[value]


def is_rain(code):
    return code in RAIN_CODES

def is_snow(code):
    return code in SNOW_CODES

def is_sun(code):
    return code in SUNNY_CODES

def is_clouds(code):
    return code in CLOUD_CODES

def is_fog(code):
    return code in FOG_CODES

def get_weather_url(latitude, longitude):
    return f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode&timezone=auto&forecast_days=1"

def query_weather_code(url):
    # type: (str) -> int
    """
    Queries the weather API for the current weather for the current location.
    Returns the numeric WMO weather code. Returns -1 it not found.

    TODO: Be smarter about choosing the day/time of the weather code.
    """

    code = -1
    with urequests.get(url) as resp:
        try:
            print("status=:", resp.status_code)
            code = resp.json()['daily']['weathercode'][0]
        except Exception as e:
            print("Caught error querying weather API:", e)

    return code

def query_weather(latitude, longitude):
    # type:  (float, float) -> WeatherValue
    """
    Query the weather for the given lat/long.
    @return a WeatherValue
    """
    url = get_weather_url(latitude, longitude)
    code = query_weather_code(url)

    # Convert the weather code into a coarse WeatherValue
    if is_sun(code):
        return WeatherValue.SUN
    if is_clouds(code):
        return WeatherValue.CLOUDS
    if is_rain(code):
        return WeatherValue.RAIN
    if is_snow(code):
        return WeatherValue.SNOW
    if is_fog(code):
        return WeatherValue.FOG
    
    print("Unrecognized weather code ", code)
    return WeatherValue.UNKNOWN
