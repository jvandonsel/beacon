
# Weather Beacon for ESP32

This project is meant to replicate the weather beacon from the [Berkley Building](https://en.wikipedia.org/wiki/Berkeley_Building), formerly known as the Old John Hancock Building.


## The Berkely Building
There's a well-known mnemonic for the color scheme of the Berkley Building beacon:

<em>

>Steady blue, clear view.
>
>Flashing blue, clouds due.
>
>Steady red, rain ahead.
>
>Flashing red, snow instead.
</em>

## Materials
TODO


## Construction
I obtained an old ship's lantern on EBay.

## Software Notes
This is my first time using [MicroPython](https://docs.micropython.org). It certainly has some deficiencies, especially when it comes to threading, but it's quicker to throw projects together in MicroPython than writing directly to the Espressif IDF API in C.

## Weather API
I'm using [OpenMeteo](https://open-meteo.com/en/docs) for the weather API.  My first choice was the [National Weather Service API](https://www.weather.gov/documentation/services-web-api) but the SSL certificate logic in MicroPython choked on the site.

## Usage Notes
TODO


