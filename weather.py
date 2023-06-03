import urequests
from utils import get_local_time

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
}

THUNDERSTORM_CODES = {
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

utc_offset_hours = 0

def get_utc_offset_hours():
    return utc_offset_hours


# Coarse weather classification, sorted from least severe to most severe
class WeatherValue:
    LEAST_SEVERE = 0
    SUN = 0
    CLOUDS = 1
    FOG = 2
    RAIN = 3
    SNOW = 4
    THUNDERSTORM = 4
    UNKNOWN = 6

    weather_value_to_string = {
        UNKNOWN: "UNKNOWN",
        SUN: "SUN",
        RAIN: "RAIN",
        SNOW: "SNOW",
        CLOUDS: "CLOUDS",
        FOG: "FOG",
        THUNDERSTORM: "THUNDERSTORM"
    }

    def to_string(value):
        return WeatherValue.weather_value_to_string[value]


def is_rain(code):
    return code in RAIN_CODES

def is_thunderstorm(code):
    return code in THUNDERSTORM_CODES

def is_snow(code):
    return code in SNOW_CODES

def is_sun(code):
    return code in SUNNY_CODES

def is_clouds(code):
    return code in CLOUD_CODES

def is_fog(code):
    return code in FOG_CODES


def query_weather_value(latitude, longitude):
    # type: (float, float) -> WeatherValue
    """
    Queries the weather API and returns a forecast for the current location
    for the next few hours.
    
    Returns WeatherValue.UNKNOWN if not found.
    """

    # Query the hourly forecast for 2 days, so we can look forward
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=weathercode&timezone=auto&forecast_days=2"

    most_severe_value = WeatherValue.LEAST_SEVERE
    resp = None
    try:
        # Query the weather
        resp = urequests.get(url)
        resp_json = resp.json()

        global utc_offset_hours
        utc_offset_hours = int(resp_json['utc_offset_seconds']) / 3600
        print("Using UTC offset=", utc_offset_hours)

        # Fetch local time
        (hour, minute) = get_local_time(utc_offset_hours)
        print("Using local hour ", hour)

        # Determine the most severe weather during the next LOOKAHEAD_HOURS.
        # The JSON weather was queried for 2 days and the hourly data
        # is contiguous, so don't wrap at a day.
        LOOKAHEAD_HOURS = 8
        for h in range(hour + 1, hour + LOOKAHEAD_HOURS):
            value = weather_code_to_value(resp_json['hourly']['weathercode'][h])
            if value > most_severe_value:
                most_severe_value = value

    except Exception as e:
            print("Caught error querying weather API:", e)
            most_severe_value = WeatherValue.UNKNOWN
    finally:
        if resp:
            resp.close()

    return most_severe_value


def weather_code_to_value(code):
    # type: (int) -> WeatherValue
    """
    Convert a WMO weather code into a coarse weather value.
    @return a WeatherValue
    """
    if is_sun(code):
        return WeatherValue.SUN
    if is_clouds(code):
        return WeatherValue.CLOUDS
    if is_rain(code):
        return WeatherValue.RAIN
    if is_thunderstorm(code):
        return WeatherValue.THUNDERSTORM
    if is_snow(code):
        return WeatherValue.SNOW
    if is_fog(code):
        return WeatherValue.FOG
    
    print("Unrecognized weather code ", code)
    return WeatherValue.UNKNOWN


