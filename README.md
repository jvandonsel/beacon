


https://api.weather.gov/gridpoints/BOX/65,89/forecast


{
    "@context": [
        "https://geojson.org/geojson-ld/geojson-context.jsonld",
        {
            "@version": "1.1",
            "wx": "https://api.weather.gov/ontology#",
            "geo": "http://www.opengis.net/ont/geosparql#",
            "unit": "http://codes.wmo.int/common/unit/",
            "@vocab": "https://api.weather.gov/ontology#"
        }
    ],
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    -71.261357599999997,
                    42.375991800000001
                ],
                [
                    -71.26648209999999,
                    42.354587000000002
                ],
                [
                    -71.237500999999995,
                    42.350796500000001
                ],
                [
                    -71.232370499999988,
                    42.372201000000004
                ],
                [
                    -71.261357599999997,
                    42.375991800000001
                ]
            ]
        ]
    },
    "properties": {
        "updated": "2023-04-22T22:09:50+00:00",
        "units": "us",
        "forecastGenerator": "BaselineForecastGenerator",
        "generatedAt": "2023-04-22T23:07:25+00:00",
        "updateTime": "2023-04-22T22:09:50+00:00",
        "validTimes": "2023-04-22T16:00:00+00:00/P8DT6H",
        "elevation": {
            "unitCode": "wmoUnit:m",
            "value": 9.1440000000000001
        },
        "periods": [
            {
                "number": 1,
                "name": "Tonight",
                "startTime": "2023-04-22T19:00:00-04:00",
                "endTime": "2023-04-23T06:00:00-04:00",
                "isDaytime": false,
                "temperature": 49,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": 80
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 7.7777777777777777
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 86
                },
                "windSpeed": "9 mph",
                "windDirection": "E",
                "icon": "https://api.weather.gov/icons/land/night/rain_showers,50/tsra,80?size=medium",
                "shortForecast": "Patchy Fog",
                "detailedForecast": "Rain showers likely before 4am, then rain showers likely and patchy fog between 4am and 5am, then patchy fog and showers and thunderstorms. Cloudy, with a low around 49. East wind around 9 mph. Chance of precipitation is 80%. New rainfall amounts between a tenth and quarter of an inch possible."
            },
            {
                "number": 2,
                "name": "Sunday",
                "startTime": "2023-04-23T06:00:00-04:00",
                "endTime": "2023-04-23T18:00:00-04:00",
                "isDaytime": true,
                "temperature": 56,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": 100
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 9.4444444444444446
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 89
                },
                "windSpeed": "12 mph",
                "windDirection": "E",
                "icon": "https://api.weather.gov/icons/land/day/tsra,100?size=medium",
                "shortForecast": "Patchy Fog",
                "detailedForecast": "Patchy fog and showers and thunderstorms. Cloudy, with a high near 56. East wind around 12 mph. Chance of precipitation is 100%. New rainfall amounts between a half and three quarters of an inch possible."
            },
            {
                "number": 3,
                "name": "Sunday Night",
                "startTime": "2023-04-23T18:00:00-04:00",
                "endTime": "2023-04-24T06:00:00-04:00",
                "isDaytime": false,
                "temperature": 47,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": 50
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 9.4444444444444446
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 86
                },
                "windSpeed": "3 to 9 mph",
                "windDirection": "NE",
                "icon": "https://api.weather.gov/icons/land/night/rain_showers,50/rain_showers,20?size=medium",
                "shortForecast": "Chance Rain Showers then Patchy Fog",
                "detailedForecast": "A chance of rain showers before 11pm, then patchy fog and a slight chance of rain showers. Cloudy, with a low around 47. Northeast wind 3 to 9 mph. Chance of precipitation is 50%. New rainfall amounts between a tenth and quarter of an inch possible."
            },
            {
                "number": 4,
                "name": "Monday",
                "startTime": "2023-04-24T06:00:00-04:00",
                "endTime": "2023-04-24T18:00:00-04:00",
                "isDaytime": true,
                "temperature": 58,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": 40
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 7.2222222222222223
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 86
                },
                "windSpeed": "5 to 9 mph",
                "windDirection": "NW",
                "icon": "https://api.weather.gov/icons/land/day/rain_showers,20/rain_showers,40?size=medium",
                "shortForecast": "Chance Rain Showers",
                "detailedForecast": "A chance of rain showers and patchy fog. Mostly cloudy, with a high near 58. Northwest wind 5 to 9 mph. Chance of precipitation is 40%. New rainfall amounts less than a tenth of an inch possible."
            },
            {
                "number": 5,
                "name": "Monday Night",
                "startTime": "2023-04-24T18:00:00-04:00",
                "endTime": "2023-04-25T06:00:00-04:00",
                "isDaytime": false,
                "temperature": 42,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": 40
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 5.5555555555555554
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 86
                },
                "windSpeed": "8 mph",
                "windDirection": "NW",
                "icon": "https://api.weather.gov/icons/land/night/rain_showers,40/rain_showers,20?size=medium",
                "shortForecast": "Chance Rain Showers",
                "detailedForecast": "A chance of rain showers. Mostly cloudy, with a low around 42. Northwest wind around 8 mph. Chance of precipitation is 40%."
            },
            {
                "number": 6,
                "name": "Tuesday",
                "startTime": "2023-04-25T06:00:00-04:00",
                "endTime": "2023-04-25T18:00:00-04:00",
                "isDaytime": true,
                "temperature": 59,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": 50
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 3.3333333333333335
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 81
                },
                "windSpeed": "7 to 10 mph",
                "windDirection": "NW",
                "icon": "https://api.weather.gov/icons/land/day/rain_showers,30/rain_showers,50?size=medium",
                "shortForecast": "Chance Rain Showers",
                "detailedForecast": "A chance of rain showers. Partly sunny, with a high near 59. Northwest wind 7 to 10 mph. Chance of precipitation is 50%."
            },
            {
                "number": 7,
                "name": "Tuesday Night",
                "startTime": "2023-04-25T18:00:00-04:00",
                "endTime": "2023-04-26T06:00:00-04:00",
                "isDaytime": false,
                "temperature": 40,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": 40
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 3.8888888888888888
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 81
                },
                "windSpeed": "6 to 9 mph",
                "windDirection": "NW",
                "icon": "https://api.weather.gov/icons/land/night/rain_showers,40/bkn?size=medium",
                "shortForecast": "Chance Rain Showers then Mostly Cloudy",
                "detailedForecast": "A chance of rain showers before 11pm. Mostly cloudy, with a low around 40. Northwest wind 6 to 9 mph. Chance of precipitation is 40%."
            },
            {
                "number": 8,
                "name": "Wednesday",
                "startTime": "2023-04-26T06:00:00-04:00",
                "endTime": "2023-04-26T18:00:00-04:00",
                "isDaytime": true,
                "temperature": 59,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": null
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 2.7777777777777777
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 81
                },
                "windSpeed": "6 to 10 mph",
                "windDirection": "W",
                "icon": "https://api.weather.gov/icons/land/day/sct/rain_showers?size=medium",
                "shortForecast": "Mostly Sunny then Slight Chance Rain Showers",
                "detailedForecast": "A slight chance of rain showers after 1pm. Mostly sunny, with a high near 59. West wind 6 to 10 mph."
            },
            {
                "number": 9,
                "name": "Wednesday Night",
                "startTime": "2023-04-26T18:00:00-04:00",
                "endTime": "2023-04-27T06:00:00-04:00",
                "isDaytime": false,
                "temperature": 42,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": null
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 3.3333333333333335
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 82
                },
                "windSpeed": "5 to 9 mph",
                "windDirection": "S",
                "icon": "https://api.weather.gov/icons/land/night/rain_showers/bkn?size=medium",
                "shortForecast": "Slight Chance Rain Showers then Mostly Cloudy",
                "detailedForecast": "A slight chance of rain showers before 9pm. Mostly cloudy, with a low around 42. South wind 5 to 9 mph."
            },
            {
                "number": 10,
                "name": "Thursday",
                "startTime": "2023-04-27T06:00:00-04:00",
                "endTime": "2023-04-27T18:00:00-04:00",
                "isDaytime": true,
                "temperature": 58,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": 30
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 3.8888888888888888
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 81
                },
                "windSpeed": "5 to 10 mph",
                "windDirection": "NE",
                "icon": "https://api.weather.gov/icons/land/day/rain_showers/rain_showers,30?size=medium",
                "shortForecast": "Chance Rain Showers",
                "detailedForecast": "A chance of rain showers after 8am. Partly sunny, with a high near 58. Northeast wind 5 to 10 mph. Chance of precipitation is 30%."
            },
            {
                "number": 11,
                "name": "Thursday Night",
                "startTime": "2023-04-27T18:00:00-04:00",
                "endTime": "2023-04-28T06:00:00-04:00",
                "isDaytime": false,
                "temperature": 41,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": 30
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 4.4444444444444446
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 89
                },
                "windSpeed": "6 to 10 mph",
                "windDirection": "NE",
                "icon": "https://api.weather.gov/icons/land/night/rain_showers,30/rain_showers?size=medium",
                "shortForecast": "Chance Rain Showers",
                "detailedForecast": "A chance of rain showers before 4am. Mostly cloudy, with a low around 41. Northeast wind 6 to 10 mph. Chance of precipitation is 30%."
            },
            {
                "number": 12,
                "name": "Friday",
                "startTime": "2023-04-28T06:00:00-04:00",
                "endTime": "2023-04-28T18:00:00-04:00",
                "isDaytime": true,
                "temperature": 57,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": null
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 3.8888888888888888
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 85
                },
                "windSpeed": "7 to 12 mph",
                "windDirection": "NE",
                "icon": "https://api.weather.gov/icons/land/day/bkn/rain_showers?size=medium",
                "shortForecast": "Partly Sunny then Slight Chance Rain Showers",
                "detailedForecast": "A slight chance of rain showers after noon. Partly sunny, with a high near 57. Northeast wind 7 to 12 mph."
            },
            {
                "number": 13,
                "name": "Friday Night",
                "startTime": "2023-04-28T18:00:00-04:00",
                "endTime": "2023-04-29T06:00:00-04:00",
                "isDaytime": false,
                "temperature": 40,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": null
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 3.3333333333333335
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 86
                },
                "windSpeed": "8 to 12 mph",
                "windDirection": "NE",
                "icon": "https://api.weather.gov/icons/land/night/rain_showers/bkn?size=medium",
                "shortForecast": "Slight Chance Rain Showers then Mostly Cloudy",
                "detailedForecast": "A slight chance of rain showers before 9pm. Mostly cloudy, with a low around 40. Northeast wind 8 to 12 mph."
            },
            {
                "number": 14,
                "name": "Saturday",
                "startTime": "2023-04-29T06:00:00-04:00",
                "endTime": "2023-04-29T18:00:00-04:00",
                "isDaytime": true,
                "temperature": 59,
                "temperatureUnit": "F",
                "temperatureTrend": null,
                "probabilityOfPrecipitation": {
                    "unitCode": "wmoUnit:percent",
                    "value": null
                },
                "dewpoint": {
                    "unitCode": "wmoUnit:degC",
                    "value": 3.3333333333333335
                },
                "relativeHumidity": {
                    "unitCode": "wmoUnit:percent",
                    "value": 83
                },
                "windSpeed": "8 to 14 mph",
                "windDirection": "E",
                "icon": "https://api.weather.gov/icons/land/day/bkn/rain_showers?size=medium",
                "shortForecast": "Partly Sunny then Slight Chance Rain Showers",
                "detailedForecast": "A slight chance of rain showers after noon. Partly sunny, with a high near 59. East wind 8 to 14 mph."
            }
        ]
    }
}
