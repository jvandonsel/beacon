import urequests
from utils import get_utc_hours

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

local_hour = 0

def get_local_hour():
    """
    The Weather module has access to the UTC TZ offset, so we'll vend local time here.
    """
    return local_hour

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



def query_weather_code(latitude, longitude):
    # type: (float, float) -> int
    """
    Queries the weather API for the current weather for the current location.
    Returns the numeric WMO weather code. Returns -1 it not found.
    """

    # Query the hourly forecast for 1 day
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=weathercode&timezone=auto&forecast_days=1"

    code = -1
    resp = None
    try:
        # Query the weather
        resp = urequests.get(url)
        resp_json = resp.json()

        # Determine UTC time hours
        utc_hours = get_utc_hours()
        if utc_hours == -1:
            # NTP in micropython is flaky. Just keep on keepin on.
            utc_hours = 0
        
        utc_offset_hours = int(resp_json['utc_offset_seconds']) / 3600
        print("Using UTC offset=", utc_offset_hours)

        # FIXME: wrapping is not correct here. We would cross days.
        global local_hour
        local_hour = int((utc_hours + utc_offset_hours) % 24)

        print("Using local hour ", local_hour)

        # Collect a histogram of the weather codes for the day, starting with the current local_hour
        map = {}
        for h in range(local_hour, 23):
            code = resp_json['hourly']['weathercode'][h]
            map[code] = map.get(code, 0) + 1

        # Find the most common weather code
        max_count = 0
        code = -1
        for k, v in map.items():
            if v > max_count:
                max_count = v
                code = k
        
    except Exception as e:
            print("Caught error querying weather API:", e)
    finally:
        if resp:
            resp.close()

    return code

def query_weather(latitude, longitude):
    # type:  (float, float) -> WeatherValue
    """
    Query the weather for the given lat/long.
    @return a WeatherValue
    """
    code = query_weather_code(latitude, longitude)

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
